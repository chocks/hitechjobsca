select pubdate::timestamp::date as post_date, title, url_link from jobs.so where job_location like '%Canada%' and pubdate between (now() - '1 month'::interval)::timestamp and now() order by pubdate desc;

select pubdate::timestamp::date as post_date, title, url_link from jobs.so where job_location like '%Canada%' and pubdate between (now() - '1 month'::interval)::timestamp and now() order by pubdate desc;
jobsdb=> \COPY (select pubdate::timestamp::date as post_date, title, url_link from jobs.so where job_location like '%Canada%' and pubdate between (now() - '1 month'::interval)::timestamp and now() order by pubdate desc) TO '/home/ec2-user/jun-jobs.csv' DELIMITER ',' CSV HEADER;



\COPY (select distinct post_date, title, url_link from (select pubdate::timestamp::date as post_date, title, url_link from jobs.so where job_location like '%Canada%' and pubdate between (now() - '1 month'::interval)::timestamp and now() union all SELECT created_at::timestamp::date as post_date, title, url_link FROM jobs.gh WHERE job_location like '%Canada%' and created_at between (now() - '1 month'::interval)::timestamp and now()) order by post_date desc) TO '/home/ec2-user/jun-jobs.csv' DELIMITER ',' CSV HEADER;
