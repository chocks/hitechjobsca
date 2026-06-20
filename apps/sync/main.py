from urllib.request import urlopen
from xml.etree import ElementTree
from datetime import datetime, timedelta
from time import sleep
import psycopg2
from config import Config
import json
import requests
import re
import hashlib

CITIES = ['toronto', 'vancouver', 'ottawa', 'montreal', 'halifax', 'ontario', 'saskatoon', 'remote', 'canada',]

# SO related stuff
TOTAL_RESULTS_TAG = '{http://a9.com/-/spec/opensearch/1.1/}totalResults'
AUTHOR_NAME_TAG = '{http://www.w3.org/2005/Atom}author'
COMPANY_NAME_TAG = '{http://www.w3.org/2005/Atom}name'
UPDATED_DATE_TAG = '{http://www.w3.org/2005/Atom}updated'
LOCATION_TAG = '{http://stackoverflow.com/jobs/}location'
SO_JOBS_URL = 'https://stackoverflow.com/jobs/feed?l=Canada'
SO_UX_JOBS = 'https://stackoverflow.com/jobs/feed?l=Canada&dr=Designer'
SO_PM_JOBS = 'https://stackoverflow.com/jobs/feed?l=Canada&dr=ProductManager'
TM_URL = 'https://api.github.com/repos/TechnologyMasters/jobs/issues'


def prepare_str(string_value):
    """
    Replace single quotes and ascii encode to insert into DB
    :param string_value:
    :return:
    """
    if not string_value:
        return None

    new_string_value = string_value.replace("'", "\"")
    utf_string_value = new_string_value

    return utf_string_value


def is_canadian_city(city):
    for a_city in CITIES:
        if city.lower().find(a_city) != -1:
            return True

    return False


def parse_salary(salary_string):
    found = 'n/a'
    pattern = "\$[^\]]+"
    match_strn = []
    for match in re.findall(pattern, salary_string):
        match_strn.append(match)
    if match_strn:
        found = ''.join(match_strn)
    final_found = found.split('\r\n')[0].split('(')[0]
    return final_found


def tm_jobs(start_time, app_config):
    date = datetime.now().date()
    print("%s: Downloading TM jobs from GitHub.." % start_time)
    tm_feed = requests.get(TM_URL)
    tm_filename = app_config.get_data_folder() + 'tm_jobs-{}.json'.format(date)
    with open(tm_filename, 'w+') as outfile:
        json.dump(tm_feed.json(), outfile)
    print('TM Download complete! processing..')
    with open(tm_filename) as f:
        data = json.load(f)

    print("Connecting to postgres db...")
    conn = psycopg2.connect(host=app_config.get_db_host(),
                            database=app_config.get_db_name(),
                            user=app_config.get_db_user(),
                            password=app_config.get_db_password())
    cur = conn.cursor()

    print("DB connected!")

    try:
        sql = """
                INSERT INTO jobs (created_at, updated_at,location, title, apply,
                company_name, salary)
                VALUES('{}', '{}', '{}', '{}','{}', '{}', '{}');
                """
        sql_statement = sql

        for item in data:
            try:
                all_items = item.get('title').split(' - ')
                company_name = all_items[0]
                title = all_items[1] if len(all_items) > 1 else 'n/a'
                location = all_items[2] if len(all_items) > 2 else 'n/a'
                apply_url = item.get('html_url')
                body = item.get('body')
                body_values = body.split('###')
                from_date = datetime.strptime(item.get('created_at'), '%Y-%m-%dT%H:%M:%SZ')
                salary_range = parse_salary(body_values[1]) if len(body_values) > 1 else 'n/a'
                if location and is_canadian_city(location):
                    sql_statement = cur.mogrify(sql.format(from_date,
                                                           from_date, location,
                                                           title, apply_url,
                                                           company_name,
                                                           salary_range
                                                           )
                                                )
                    cur.execute(sql_statement)
                    conn.commit()
            except psycopg2.IntegrityError:
                print('dup job, skipping..')
                conn.commit()
            except (ValueError, TypeError, IndexError):
                print('bad formatting, skipping..')
    except (Exception, psycopg2.DatabaseError) as error:
        print('sqlerror', error)
        print(sql_statement)
    finally:
        if conn is not None:
            conn.close()
    print("TM GH job done!")


def so_jobs_feed(start_time, app_config, jobs_url, job_type):
    print("{}: Downloading jobs rss feed from stack overflow {} jobs..".format(start_time, job_type))
    feed = urlopen(jobs_url)
    data = feed.read()
    feed.close()

    today = datetime.today().date()
    xml_file_name = app_config.get_data_folder() + str(today) + '-' + job_type + '.xml'
    xml_file = open(xml_file_name, 'wb')
    xml_file.write(data)
    xml_file.close()
    print('RSS feed download complete! processing..')

    sleep(5)
    root = ElementTree.parse(xml_file_name).getroot()
    channel = root.find('channel')
    total_results = int(channel.find(TOTAL_RESULTS_TAG).text)

    all_jobs = channel.findall('item')

    if len(all_jobs) != total_results:
        print("Data validation failed!!")
        return

    print("Data validation success! Proceeding..")
    print("Connecting to postgres db...")
    conn = psycopg2.connect(host=app_config.get_db_host(),
                            database=app_config.get_db_name(),
                            user=app_config.get_db_user(),
                            password=app_config.get_db_password())
    cur = conn.cursor()

    print("DB connected!")

    sql = """
        INSERT INTO jobs (created_at, updated_at,location, title, apply,
        company_name, salary)
        VALUES('{}', '{}', '{}', '{}','{}', '{}', '{}');
        """
    sql_statement = sql
    try:
        for job in all_jobs:
            location = prepare_str(job.find(LOCATION_TAG).text) if job.find(LOCATION_TAG) is not None else None

            apply_url = job.find('link').text if job.find('link') is not None else None

            author_name = job.find(AUTHOR_NAME_TAG)
            company_name = prepare_str(author_name.find(COMPANY_NAME_TAG).text) \
                if author_name.find(COMPANY_NAME_TAG) is not None else None

            title = prepare_str(job.find('title').text[:128]) if job.find('title') is not None else None
            from_date = datetime.strptime(job.find(UPDATED_DATE_TAG).text if job.find(UPDATED_DATE_TAG) is not None
                                          else '%Y-%m-%dT%H:%M:%SZ'.format(datetime.now()), '%Y-%m-%dT%H:%M:%SZ')
            salary_range = 'n/a'
            apply_link_hash = hashlib.sha256()
            apply_link_hash.update(apply_url.encode("utf8"))
            try:
                sql_statement = cur.mogrify(sql.format(from_date,
                                                       from_date,
                                                       location,
                                                       title, apply_url,
                                                       company_name,
                                                       salary_range
                                                       )
                                            )
                cur.execute(sql_statement)
                conn.commit()
            except psycopg2.IntegrityError as exp:
                print('dup job, skipping..')
                conn.commit()
        print("So job done!")
    except (Exception, psycopg2.DatabaseError) as error:
        print('sqlerror', error)
        print(sql_statement)
    finally:
        if conn is not None:
            conn.close()


app_config = Config()

start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("\n\n#################################################\n\n")
so_jobs_feed(start_time, app_config, SO_JOBS_URL, 'all')
end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("\n\n#################################################\n\n")

start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("\n\n#################################################\n\n")
so_jobs_feed(start_time, app_config, SO_PM_JOBS, 'pm')
end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("\n\n#################################################\n\n")

start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("\n\n#################################################\n\n")
so_jobs_feed(start_time, app_config, SO_UX_JOBS, 'ux')
end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("\n\n#################################################\n\n")

start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("\n\n#################################################\n\n")
tm_jobs(start_time, app_config)
end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("%s: All done, go home!" % end_time)
print("\n\n#################################################\n\n")
