CREATE TABLE jobs.order_job (
        id SERIAL PRIMARY KEY,
        order_id integer REFERENCES orders (id),
        job_id integer REFERENCES all_jobs (id)
);
