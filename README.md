# HiTechJobs.CA

> Find the latest tech jobs in Canada — a jobs board and lightweight ATS,
> built and launched from Toronto. 🇨🇦

**Status:** archived. The live site (`hitechjobs.ca`) is no longer running.
This repository consolidates the original two projects into a single monorepo
so the code stays together and runnable.

## Monorepo layout

```
hitechjobsca/
├── apps/
│   ├── web/    # React + Redux frontend (job listings, search, post-a-job)
│   ├── api/    # Spring Boot REST API backed by PostgreSQL full-text search
│   └── sync/   # Python ingest: Stack Overflow RSS + GitHub issues → Postgres
├── db/init/    # Postgres schema + seed data
└── docker-compose.yml
```

### apps/web — frontend
React 16 + Redux + React Router, built with **Vite**. Talks to the API for
`/ca_jobs` (listings), `/search` (Postgres full-text search), and `/new`
(post a job, with Stripe checkout). Run `npm run dev` for the dev server or
`npm run build` for a production bundle (`dist/`).

### apps/api — REST API
Spring Boot 3.3 (Java 21 LTS), Spring Data JPA over PostgreSQL. Search is powered by
a Postgres `tsvector` column with a `gin` index and an insert trigger, so
listings are full-text searchable by title, company, and location.

### apps/sync — jobs ingest
Python ingest that pulls Canadian tech listings from a GitHub issues feed
(`TechnologyMasters/jobs`) into Postgres, upserting into `jobs.all_jobs` keyed
on `ext_id` (idempotent). The original Stack Overflow jobs RSS source is
preserved but its feed was discontinued in 2023 (404/403 → skipped gracefully).
Async httpx fetch, parameterized batch upsert, uv-managed deps, and a pytest
suite. Run it once, or on a loop (`SYNC_INTERVAL_SECONDS`) as a sidecar:

```bash
docker compose up -d db
docker compose --profile sync run --rm sync
# dry-run (fetch + parse, no DB write):
docker compose --profile sync run --rm -e SYNC_DRY_RUN=1 sync
# loop as a sidecar (every hour):
docker compose --profile sync run --rm -e SYNC_INTERVAL_SECONDS=3600 sync
```

Locally with uv (tests included):

```bash
cd apps/sync
uv sync --extra dev && uv run pytest      # test suite (no DB needed)
DB_HOST=localhost DB_NAME=jodb DB_USER=developer \
    DB_PASSWORD=developer uv run python main.py
```

Config comes from env vars (`DB_HOST`/`DB_PORT`/`DB_NAME`/`DB_USER`/
`DB_PASSWORD`/`DATA_FOLDER`, plus `SYNC_INTERVAL_SECONDS`, `SYNC_DRY_RUN`,
`SYNC_GITHUB_TOKEN`, `SYNC_REQUEST_TIMEOUT`); see `.env.example`. A Hacker
News "Who is hiring?" source is on the roadmap.

## Run it locally

Requires Docker. From the repo root:

```bash
cp .env.example .env          # optional; sensible dev defaults otherwise
docker compose up --build
```

- Frontend: <http://localhost:3000>
- API: <http://localhost:8080> (`/ca_jobs`, `/search?searchString=engineer`)

`docker compose up` starts three services: **Postgres** (seeded with sample
Canadian tech listings + the full-text search trigger), the **Spring Boot API**
(built in-container with Maven/JDK 21), and **nginx** serving the frontend and
reverse-proxying the API paths so the browser talks to it same-origin.

## Press & mentions

The site picked up some coverage back when it was live:

- [How to search for jobs in Toronto — blogTO](https://www.blogto.com/city/2011/01/how_to_search_for_jobs_in_toronto/)
- [HiTechJobs.CA on Product Hunt](https://www.producthunt.com/products/hitechjobsca)
- [Product Hunt newsletter feature](https://www.producthunt.com/newsletter/2436)

## Security note

This is preserved as the original 2020 application. It carries known issues
that make it **unsafe to deploy publicly as-is** — notably no authentication on
`POST /new` and a stubbed payment flow that records orders as paid without
verifying a real charge. These are tracked in the roadmap and called out in
[CLAUDE.md](CLAUDE.md); they should be addressed before any re-launch.

## Roadmap

This repo is being brought back to life incrementally:

- [x] Consolidate `jobs-frontend` + `jobs-rest-api` into one monorepo
- [x] Scrub credentials; configure the API via environment variables
- [x] Dockerize the full stack (`docker compose up`: Postgres + API + nginx)
- [x] Modernize the frontend toolchain (Webpack 1 → Vite); drop the committed
      `bundle.js`
- [ ] Modernize the frontend framework — upgrade React 16 → React 19 (or
      rewrite in Vue 3). Bigger lift; a later improvement.
- [x] Modernize the API (Spring Boot 1.5 → 3.3, Java 8 → 21 LTS; javax →
      jakarta persistence, Hibernate 6 dialect; drop dead `Config` + Gradle
      build files)
- [x] Wire `apps/sync` into `jobs.all_jobs` — adapt the `INSERT INTO jobs (...)`
      column set to the current schema (`apply_url`, `salary_range`, `ext_id`,
      …) so ingest actually populates the board
- [x] Modernize `apps/sync` — async/httpx client, parameterized batch upsert,
      tests, uv-managed deps; dead SO RSS handled gracefully; GitHub issues
      feed wired to `jobs.all_jobs`. Runnable once or on a loop
      (`SYNC_INTERVAL_SECONDS`) as a sidecar.
- [ ] Add a Hacker News "Who is hiring?" source to `apps/sync` — the monthly
      [Ask HN: Who is hiring?](https://news.ycombinator.com/item?id=48357725)
      thread is a rich, remote-friendly feed with Canadian postings (e.g.
      "REMOTE (MUST LIVE IN CANADA)"). Pull comments via the HN/Algolia API,
      filter by the existing Canadian-city allowlist, and normalize into
      `jobs.all_jobs` like the other sources.
- [ ] Schedule `apps/sync` (cron/sidecar) now that it is schema-aligned
- [ ] Add authentication + real payment verification to `POST /new`
- [x] Add CI (pre-commit hooks + Docker build, and run tests once they exist) —
      GitHub Actions: pre-commit/gitleaks/hadolint, `apps/sync` pytest,
      `apps/api` Maven build, `apps/web` Vite build, and a `docker compose
      build` of all three images. A `Makefile` wraps local dev
      (`make run` → `docker compose up --build`) and per-app tests.

## Development

`main` is protected — contribute via a branch and a pull request (no direct
pushes). Optional git hygiene + secret scanning via
[pre-commit](https://pre-commit.com):

```bash
pre-commit install
pre-commit run --all-files
```

A `Makefile` wraps the common workflows (Docker stack, per-app dev/tests,
pre-commit). `make help` lists every target:

```bash
make run          # db + api + web via docker compose (foreground, builds first)
make up           # same, detached
make down         # stop and remove containers
make test         # apps/sync pytest + apps/api mvn test + apps/web vite build
make sync         # run the jobs ingest once (needs the db service up)
make precommit    # run pre-commit across all files
```

CI runs on every push/PR to `main` via `.github/workflows/ci.yml`: pre-commit
(gitleaks + hadolint), `apps/sync` pytest, `apps/api` Maven build, `apps/web`
Vite build, and a `docker compose build` of all three images.

## License

[MIT](LICENSE) © Chocks Eswaramurthy
