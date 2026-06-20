# sync app: fetches Canadian tech jobs (GitHub issues + legacy SO RSS) and
# upserts them into Postgres jobs.all_jobs. Runs once by default; set
# SYNC_INTERVAL_SECONDS to run on a loop as a sidecar. uv-managed deps.
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH=/app/.venv/bin:$PATH

WORKDIR /app

# Install deps first for better layer caching. --frozen uses the committed
# uv.lock; --no-dev skips the test toolchain from the production image.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# App source (tests/ and *.sql are dockerignored).
COPY config.py main.py db.py ./
COPY sources ./sources

ENV DATA_FOLDER=/data/
RUN mkdir -p /data
CMD ["python", "main.py"]
