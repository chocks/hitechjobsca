# apps/sync — jobs ingest

Fetches Canadian tech job listings from two sources and loads them into
PostgreSQL. This is the original 2020 ingest script (`myrepo/main.py`)
dropped into the monorepo **as-is**, with only the minimum needed to run it
from Docker and to keep secrets out of git:

- `config.py` reads DB credentials and the data folder from environment
  variables first, falling back to the original `/etc/opt/jobs-download/.config`
  file when env vars are absent. No other behavior changed.
- `scripts/sendemail.sh` had a hardcoded RDS hostname; it now reads
  `PGHOST`/`PGUSER`/`PGDATABASE` from the environment.

## Sources

- **Stack Overflow jobs RSS** (`so_jobs_feed`) — Canada, Product Manager, and
  Designer feeds. Saved to `<DATA_FOLDER>/<date>-{all,pm,ux}.xml`.
- **GitHub issues** (`tm_jobs`) — `TechnologyMasters/jobs` issues, fetched via
  the GitHub API and saved to `<DATA_FOLDER>/tm_jobs-<date>.json`.

Each listing is inserted into the `jobs` table (see `main.py`). Duplicate
inserts are caught and skipped.

## Run it from Docker

The `sync` service is behind a Compose profile so it does **not** start with
the rest of the stack. Bring up the DB first, then run the sync once:

```bash
docker compose up -d db                 # start Postgres
docker compose --profile sync run --rm sync
```

Downloaded XML/JSON land in the `syncdata` volume (`/data` in the container).

Outside Docker, with a Postgres reachable:

```bash
cd apps/sync
pip install -r requirements.txt
DB_HOST=localhost DB_NAME=jodb DB_USER=developer DB_PASSWORD=developer \
    DATA_FOLDER=./data/ python main.py
```

## Known gaps (modernization is on the roadmap)

This app is preserved as-is. It is **not yet wired to the monorepo's
`jobs.all_jobs` schema** — the `INSERT INTO jobs (...)` statements target the
original 2020 column set (`created_at, updated_at, apply, salary, ...`), which
does not match `db/init/01_schema.sql`. Running it against the current
database will download the feeds successfully but fail on every insert until
the schema alignment is done. That work is tracked in the root roadmap
([../README.md](../README.md) and [CLAUDE.md](../../CLAUDE.md)).

## Layout

```
apps/sync/
├── main.py             # ingest logic (SO RSS + GitHub issues → Postgres)
├── config.py           # env-var config with config-file fallback
├── requirements.txt    # psycopg2, requests, xmltodict, python-dateutil
├── Dockerfile          # python:3.12-slim image, runs main.py once
├── scripts/            # original cron + CSV-export shell wrappers
├── sql-scripts.sql     # historical reporting queries
└── maintanence.sql     # historical maintenance queries
```
