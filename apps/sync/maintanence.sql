

delete from jobs.order_job;
delete from jobs.orders;
delete from jobs.all_jobs;

ALTER SEQUENCE jobs.order_job_id_seq RESTART;
ALTER SEQUENCE jobs.orders_id_seq RESTART;
ALTER SEQUENCE jobs.all_jobs_id_seq RESTART;

alter table jobs.all_jobs add column ext_id bigint not null;
CREATE UNIQUE INDEX idx_unq_all_jobs ON jobs.all_jobs (ext_id);
-- manually copy over posted jobs
