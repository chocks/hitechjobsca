# CLAUDE.md

Guidance for working in this repository.

## What this is

HiTechJobs.CA — an **archived** Canadian tech jobs board + lightweight ATS,
originally two separate projects (`jobs-frontend`, `jobs-rest-api`) now
consolidated into one monorepo. The live site is no longer running; the goal
is to keep the code together, runnable, and modernized incrementally.

## Contributing (branch protection)

`main` is protected — **no direct pushes**. All changes go through a branch and
a pull request:

```bash
git checkout -b feat/my-change
# ...work, commit...
git push -u origin feat/my-change
gh pr create --fill
```

## Layout

- `apps/web` — React 16 + Redux frontend, built with **Vite**. Source lives in
  `apps/web/src` (`.jsx` for components, `.js` for actions/reducers); static
  assets are in `apps/web/public` (served at `/static`, `/style`, `/seo`). The
  API base URL is set in `apps/web/src/actions/index.js` (empty string =
  same-origin via nginx). Dev: `npm run dev`; production build: `npm run build`
  → `dist/` (gitignored; built fresh in the Docker image).
- `apps/api` — Spring Boot 3.3 (Java 21 LTS) REST API, Spring Data JPA over
  PostgreSQL. Full-text search uses a `tsvector` column + `gin` index + insert
  trigger (see `db/init/01_schema.sql`). Endpoints: `GET /ca_jobs`,
  `GET /search?searchString=`, `POST /new`.
- `apps/sync` — Python ingest script. Pulls Stack Overflow RSS + GitHub issues
  into Postgres. `config.py` reads `DB_HOST`/`DB_NAME`/`DB_USER`/`DB_PASSWORD`/
  `DATA_FOLDER` from the env (config-file fallback). Behind the `sync` Compose
  profile: `docker compose --profile sync run --rm sync`. Modernized to write
  to `jobs.all_jobs` via a parameterized batch upsert keyed on `ext_id`
  (idempotent); async httpx fetch; dead SO RSS (404) is skipped gracefully and
  the live GitHub `TechnologyMasters/jobs` issues feed is the working source.
  uv-managed (`apps/sync/pyproject.toml`, `uv.lock`). Tests under
  `apps/sync/tests/` (`uv run pytest`).
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

- ~~Frontend: Webpack 1 → a current bundler~~ — done (Vite; `bundle.js` removed).
- ~~API: Spring Boot 1.5 → current; Java 8 → current LTS~~ — done (Spring Boot
  3.3, Java 21, Jakarta persistence).
- Frontend: React 16 → React 19 (or rewrite in Vue 3). Bigger lift; later.
- `apps/sync`: ~~wire the `INSERT INTO jobs (...)` column set into
  `jobs.all_jobs`~~ done; ~~modernize (async/HTTP client, parameterized
  queries, tests)~~ done (async httpx, parameterized batch upsert, pytest,
  uv-managed). Runnable once or on a loop (`SYNC_INTERVAL_SECONDS`). The dead
  Stack Overflow RSS feed is handled gracefully (404 → skip); the live GitHub
  `TechnologyMasters/jobs` issues feed is wired to `jobs.all_jobs`.
- `apps/sync`: add a Hacker News "Who is hiring?" source (monthly
  [Ask HN](https://news.ycombinator.com/item?id=48357725) thread → comments via
  the HN/Algolia API → filter by the Canadian-city allowlist →
  `jobs.all_jobs`). Scheduling the ingest (cron/sidecar) is also still open.
- The original app has **no auth on `POST /new`** and a stubbed payment flow
  (`Orders(contact, description)` fabricates a paid order). This is legacy
  behavior preserved as-is, not safe for a public deployment — see the
  Security section in the README before re-launching.
