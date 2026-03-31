FROM node:20-alpine AS css-builder

WORKDIR /app

COPY package.json ./
COPY tailwind.config.js postcss.config.js ./
COPY static/src ./static/src
COPY templates ./templates
COPY apps ./apps

RUN npm install
RUN npm run build:css

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements ./requirements
RUN pip install --no-cache-dir -r requirements/production.txt

COPY . .
COPY --from=css-builder /app/static/css/styles.css /app/static/css/styles.css

RUN useradd --create-home appuser \
    && chmod +x /app/docker/entrypoint.sh \
    && chown -R appuser:appuser /app

USER appuser

CMD ["/app/docker/entrypoint.sh", "gunicorn", "config.wsgi:application", "-c", "docker/gunicorn/gunicorn.conf.py"]
