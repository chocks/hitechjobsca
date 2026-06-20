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
│   ├── web/   # React + Redux frontend (job listings, search, post-a-job)
│   └── api/   # Spring Boot REST API backed by PostgreSQL full-text search
├── db/init/   # Postgres schema + seed data
└── docker-compose.yml
```

### apps/web — frontend
React 16 + Redux + React Router, bundled with Webpack. Talks to the API for
`/ca_jobs` (listings), `/search` (Postgres full-text search), and `/new`
(post a job, with Stripe checkout). The 2020 Webpack 1 toolchain can't build on
modern Node, so the prebuilt `bundle.js` is committed and served as-is for now.

### apps/api — REST API
Spring Boot 1.5 (Java 8), Spring Data JPA over PostgreSQL. Search is powered by
a Postgres `tsvector` column with a `gin` index and an insert trigger, so
listings are full-text searchable by title, company, and location.

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
(built in-container with Maven/JDK 8), and **nginx** serving the frontend and
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
- [ ] Modernize the frontend toolchain (Webpack 1 → current) and drop the
      committed `bundle.js`
- [ ] Modernize the API (Spring Boot 1.5 → current, Java 8 → current LTS)
- [ ] Add authentication + real payment verification to `POST /new`

## Development

Optional git hygiene + secret scanning via [pre-commit](https://pre-commit.com):

```bash
pre-commit install
pre-commit run --all-files
```

## License

[MIT](LICENSE) © Chocks Eswaramurthy
