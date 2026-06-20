-- create table
CREATE TABLE jobs.all_jobs (
        id SERIAL PRIMARY KEY,
        title varchar(128) NOT NULL,
        company_name varchar(128) NOT NULL,
        apply_url varchar(256) NOT NULL,
        salary_range varchar(64) NOT NULL default 'N/A',
        from_date date NOT NULL default now(),
        end_date date NOT NULL default now() + interval '60 days',
        location varchar(64) NOT NULL default 'Canada',
        search_vectors tsvector,
        pinned boolean default False,
        status boolean default False,
        rank int default 0,
        ext_id varchar(255) NOT NULL
);

-- create indices
CREATE INDEX idx_fts_doc_vec ON jobs.all_jobs USING gin(search_vectors);
CREATE UNIQUE INDEX idx_unq_all_jobs ON jobs.all_jobs (ext_id);

-- Create a pg trigger so we don't have to define custom jpa entity (not supported yet :( )
CREATE TRIGGER jobs_vector_update
BEFORE INSERT ON jobs.all_jobs
FOR EACH ROW
EXECUTE PROCEDURE tsvector_update_trigger(search_vectors, 'pg_catalog.english', title, company_name, location);


---misc updates
ALTER TABLE jobs.all_jobs ADD COLUMN "search_vectors" tsvector;
UPDATE
    jobs.all_jobs
SET
    search_vectors = (to_tsvector(title) || to_tsvector(company_name) || to_tsvector(location));
