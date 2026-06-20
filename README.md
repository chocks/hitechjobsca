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

### apps/sync — jobs ingest (as-is, not yet wired to the current schema)
The original 2020 Python script that pulls Canadian tech listings from Stack
Overflow RSS feeds and a GitHub issues feed and loads them into Postgres. Added
as-is; it is containerized and runnable, but its `INSERT INTO jobs (...)`
statements target the old column set and do not yet match `jobs.all_jobs`
(`db/init/01_schema.sql`). Schema alignment is on the roadmap. Run it once:

```bash
docker compose up -d db
docker compose --profile sync run --rm sync
```

See [apps/sync/README.md](apps/sync/README.md) for details.

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
- [ ] Wire `apps/sync` into `jobs.all_jobs` — adapt the `INSERT INTO jobs (...)`
      column set to the current schema (`apply_url`, `salary_range`, `ext_id`,
      …) so ingest actually populates the board, then schedule it (cron/sidecar)
- [ ] Modernize `apps/sync` — async/HTTP client, parameterized queries, tests
- [ ] Add authentication + real payment verification to `POST /new`
- [ ] Add CI (pre-commit hooks + Docker build, and run tests once they exist)

## Development

`main` is protected — contribute via a branch and a pull request (no direct
pushes). Optional git hygiene + secret scanning via
[pre-commit](https://pre-commit.com):

```bash
pre-commit install
pre-commit run --all-files
```

## License

[MIT](LICENSE) © Chocks Eswaramurthy
