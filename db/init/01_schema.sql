-- HiTechJobs.CA schema. Runs once on first Postgres init
-- (docker-entrypoint-initdb.d). The API also has ddl-auto=update, so this is
-- primarily here to set up the full-text search column + trigger that
-- Hibernate can't express, and to seed a few sample listings.

CREATE SCHEMA IF NOT EXISTS jobs;

-- Job listings -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS jobs.all_jobs (
    id             SERIAL PRIMARY KEY,
    title          varchar(128) NOT NULL,
    company_name   varchar(128) NOT NULL,
    apply_url      varchar(256) NOT NULL,
    salary_range   varchar(64)  NOT NULL DEFAULT 'N/A',
    from_date      date         NOT NULL DEFAULT now(),
    end_date       date         NOT NULL DEFAULT now() + interval '60 days',
    location       varchar(64)  NOT NULL DEFAULT 'Canada',
    search_vectors tsvector,
    pinned         boolean      DEFAULT false,
    status         boolean      DEFAULT false,
    rank           int          DEFAULT 0,
    ext_id         varchar(255) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_fts_doc_vec ON jobs.all_jobs USING gin(search_vectors);
CREATE UNIQUE INDEX IF NOT EXISTS idx_unq_all_jobs ON jobs.all_jobs (ext_id);

-- Keep the full-text search vector in sync with title/company/location.
CREATE TRIGGER jobs_vector_update
BEFORE INSERT OR UPDATE ON jobs.all_jobs
FOR EACH ROW EXECUTE PROCEDURE
    tsvector_update_trigger(search_vectors, 'pg_catalog.english',
                            title, company_name, location);

-- Orders (post-a-job purchases) ------------------------------------------
CREATE TABLE IF NOT EXISTS jobs.orders (
    id          BIGSERIAL PRIMARY KEY,
    token       varchar(256),
    status      boolean       NOT NULL DEFAULT true,
    contact     varchar(256)  NOT NULL,
    amount      numeric(12,2) NOT NULL DEFAULT 250.00,
    currency    varchar(6)    NOT NULL DEFAULT 'CAD',
    date        date          NOT NULL DEFAULT now(),
    description varchar(64)
);

CREATE TABLE IF NOT EXISTS jobs.order_job (
    id       BIGSERIAL PRIMARY KEY,
    order_id bigint REFERENCES jobs.orders(id),
    job_id   bigint REFERENCES jobs.all_jobs(id)
);

-- Shared sequence used by Hibernate GenerationType.AUTO (orders, order_job).
CREATE SEQUENCE IF NOT EXISTS hibernate_sequence START 1;

-- Sample listings so the homepage shows data out of the box -------------
INSERT INTO jobs.all_jobs (title, company_name, apply_url, salary_range, location, status, rank, ext_id) VALUES
    ('Senior Software Engineer', 'Shopify',     'https://www.shopify.com/careers',  '$130k - $175k', 'Toronto, ON',     true, 1, 'seed-001'),
    ('Frontend Developer (React)', 'Wealthsimple', 'https://www.wealthsimple.com/careers', '$110k - $150k', 'Toronto, ON', true, 2, 'seed-002'),
    ('Backend Engineer (Java)',  'RBC',         'https://jobs.rbc.com',             '$120k - $160k', 'Toronto, ON',     true, 2, 'seed-003'),
    ('Data Engineer',            'Lightspeed',  'https://www.lightspeedhq.com/careers', '$115k - $155k', 'Montreal, QC', true, 3, 'seed-004'),
    ('DevOps / SRE',             'Hootsuite',   'https://www.hootsuite.com/careers','$125k - $165k', 'Vancouver, BC',   true, 3, 'seed-005'),
    ('Product Manager',          'Clio',        'https://www.clio.com/about/careers','$130k - $170k', 'Burnaby, BC',    false, 4, 'seed-006')
ON CONFLICT (ext_id) DO NOTHING;
