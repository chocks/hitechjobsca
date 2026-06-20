# CLAUDE.md

Guidance for working in this repository.

## What this is

HiTechJobs.CA — an **archived** Canadian tech jobs board + lightweight ATS,
originally two separate projects (`jobs-frontend`, `jobs-rest-api`) now
consolidated into one monorepo. The live site is no longer running; the goal
is to keep the code together, runnable, and modernized incrementally.

## Layout

- `apps/web` — React 16 + Redux frontend. Built in 2020 with **Webpack 1**,
  which cannot build on modern Node. The committed `apps/web/bundle.js` is the
  prebuilt artifact and is intentionally tracked until the build is modernized.
  Source lives in `apps/web/src`; the API base URL is set in
  `apps/web/src/actions/index.js` (empty string = same-origin via nginx).
- `apps/api` — Spring Boot 1.5 (Java 8) REST API, Spring Data JPA over
  PostgreSQL. Full-text search uses a `tsvector` column + `gin` index + insert
  trigger (see `db/init/01_schema.sql`). Endpoints: `GET /ca_jobs`,
  `GET /search?searchString=`, `POST /new`.
- `db/init` — Postgres schema + seed data, run once on first container init.

## Running

```bash
docker compose up --build      # Postgres + API + nginx-served frontend
# frontend: http://localhost:3000   api: http://localhost:8080
```

The API reads DB credentials from `SPRING_DATASOURCE_*` env vars (set by
docker-compose). Never hardcode credentials in `application.properties`.

## Conventions

- **No secrets in git.** DB credentials, tokens, and keys come from the
  environment / `.env` (gitignored). `.env.example` documents the variables.
- The frontend reaches the API **same-origin**; nginx (`apps/web/nginx.conf`)
  reverse-proxies `/ca_jobs`, `/new`, `/search` to the `api` service. If you
  rebuild `bundle.js`, keep `API = ''` in `src/actions/index.js`.
- When changing the DB schema, update both the JPA entities in
  `apps/api/.../data` and `db/init/01_schema.sql`.

## Known modernization debt (incremental)

- Frontend: Webpack 1 → a current bundler; then stop committing `bundle.js`.
- API: Spring Boot 1.5 → current; Java 8 → current LTS.
- The original app has **no auth on `POST /new`** and a stubbed payment flow
  (`Orders(contact, description)` fabricates a paid order). This is legacy
  behavior preserved as-is, not safe for a public deployment — see the
  Security section in the README before re-launching.
