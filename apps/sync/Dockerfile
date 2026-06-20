# sync app: fetches Canadian tech jobs from Stack Overflow RSS + a GitHub
# issues feed and loads them into Postgres. Runs once and exits; see
# scripts/cronjob.sh for the original cron wrapper.
FROM python:3.12-slim

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /data
ENV DATA_FOLDER=/data/
CMD ["python", "main.py"]
