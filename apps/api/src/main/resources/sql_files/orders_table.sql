
CREATE TABLE jobs.orders (
        id SERIAL PRIMARY KEY,
        token varchar(256) NOT NULL,
        status boolean NOT NULL,
        contact varchar(256) NOT NULL,
        amount numeric(12,2) NOT NULL default 250.00,
        currency VARCHAR(6) NOT NULL default 'CAD',
        date date NOT NULL default now(),
        description varchar(64)
);
