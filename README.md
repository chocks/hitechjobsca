# HiTechJobs.CA

> Find the latest tech jobs in Canada — a jobs board and lightweight ATS,
> built and launched from Toronto. 🇨🇦

**Status:** archived. The live site (`hitechjobs.ca`) is no longer running.
This repository consolidates the original two projects into a single monorepo
so the code stays together and runnable.

![HiTechJobs.CA screenshot](docs/screenshot.png)

## Monorepo layout

```
hitechjobsca/
├── apps/
│   ├── web/   # React + Redux frontend (job listings, search, post-a-job)
│   └── api/   # Spring Boot REST API backed by PostgreSQL full-text search
└── docs/      # screenshots & assets
```

### apps/web — frontend
React 16 + Redux + React Router, bundled with Webpack. Talks to the API for
`/ca_jobs` (listings), `/search` (Postgres full-text search), and `/new`
(post a job, with Stripe checkout).

### apps/api — REST API
Spring Boot 1.5 (Java 8), Spring Data JPA over PostgreSQL. Search is powered by
a Postgres `tsvector` column with a `gin` index and an insert trigger, so
listings are full-text searchable by title, company, and location.

## Press & mentions

The site picked up some coverage back when it was live:

- [How to search for jobs in Toronto — blogTO](https://www.blogto.com/city/2011/01/how_to_search_for_jobs_in_toronto/)
- [HiTechJobs.CA on Product Hunt](https://www.producthunt.com/products/hitechjobsca)
- [Product Hunt newsletter feature](https://www.producthunt.com/newsletter/2436)

## Roadmap

This repo is being brought back to life incrementally:

- [x] Consolidate `jobs-frontend` + `jobs-rest-api` into one monorepo
- [x] Scrub credentials; configure the API via environment variables
- [ ] Dockerize the full stack (`docker compose up`: Postgres + API + nginx)
- [ ] Modernize the frontend toolchain (Webpack 1 → current) and drop the
      committed `bundle.js`
- [ ] Modernize the API (Spring Boot 1.5 → current, Java 8 → current LTS)

## License

See [apps/web/LICENSE.MD](apps/web/LICENSE.MD).
