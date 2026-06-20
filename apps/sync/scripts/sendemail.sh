#!/usr/bin/env bash

DATE=`date +%B-%Y`
RESULTS_PATH="${DATA_FOLDER:-./data}/send-mail/$DATE.csv"
echo $RESULTS_PATH
psql -h "${PGHOST:-db}" -p "${PGPORT:-5432}" -U "${PGUSER:-developer}" "${PGDATABASE:-jodb}" -c "\COPY (select pubdate::timestamp::date as post_date, title, url_link from jobs.so where job_location like '%Canada%' and pubdate between (now() - '1 month'::interval)::timestamp and now() union all SELECT created_at::timestamp::date as post_date, title, url_link FROM jobs.gh WHERE job_location like '%Canada%' and created_at between (now() - '1 month'::interval)::timestamp and now() order by post_date desc) TO $RESULTS_PATH DELIMITER ',' CSV HEADER;"

echo "Done!"
