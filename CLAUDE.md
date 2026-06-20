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
- The original app has **no auth on `POST /new`** and a stubbed payment flow
  (`Orders(contact, description)` fabricates a paid order). This is legacy
  behavior preserved as-is, not safe for a public deployment — see the
  Security section in the README before re-launching.
