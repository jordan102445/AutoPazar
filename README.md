# AutoPazar

AutoPazar is a production-minded Django marketplace for peer-to-peer car sales in North Macedonia. It is server-rendered with Django templates and HTMX, backed by Django REST Framework for future mobile clients, and structured as a modular monolith for maintainability.

## Product scope

- User registration, login, profile management, email verification scaffold
- Car listings with rich metadata, image uploads, favorites, seller contact, reporting
- Search and filtering by relevant North Macedonia marketplace fields
- Seller dashboard for managing listings, favorites, and inquiries
- Admin moderation and audit logging
- REST API for core resources

## Architecture

The project is intentionally monolithic but split by domain:

- `apps/core`: shared models, helpers, health check, seed command
- `apps/users`: custom user model, profiles, auth flows, dashboard
- `apps/listings`: brands, models, listings, images, filters, listing management
- `apps/favorites`: saved listings
- `apps/messaging`: buyer-to-seller inquiries
- `apps/moderation`: reports and audit events
- `config/`: settings split, URL routing, Celery bootstrap

This keeps shared infrastructure centralized while business logic stays close to its domain.

## Stack

- Django + Django REST Framework
- PostgreSQL
- Redis
- Celery
- Gunicorn
- Nginx
- Tailwind CSS + HTMX
- Docker Compose
- pytest / pytest-django

## Key decisions

- Custom user model from day one to avoid migration pain later
- Reference tables for cities and car brands/models to keep filtering consistent
- Soft-delete support on listings via `deleted_at`
- HTMX for targeted progressive enhancement instead of a SPA
- DRF endpoints for future mobile or partner clients

## Local setup without Docker

Prerequisites on Ubuntu:

```bash
sudo apt update
sudo apt install python3-venv python3-pip nodejs npm postgresql redis-server libpq-dev
```

Create the local PostgreSQL database and user:

```bash
sudo -u postgres psql
CREATE USER autopazar WITH PASSWORD 'autopazar';
ALTER USER autopazar CREATEDB;
CREATE DATABASE autopazar OWNER autopazar;
\q
```

Start PostgreSQL and Redis:

```bash
sudo systemctl enable --now postgresql
sudo systemctl enable --now redis-server
```

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements/dev.txt
```

3. Install Tailwind dependencies:

```bash
npm install
npm run build:css
```

4. Copy the environment file and adjust values:

```bash
cp .env.example .env
```

For local development, `.env.example` now uses `127.0.0.1` for PostgreSQL and Redis.

5. Run migrations and seed demo data:

```bash
python manage.py migrate
python manage.py sync_reference_data
python manage.py seed_demo_data
```

6. Start the web server:

```bash
python manage.py runserver
```

7. Start Celery in a second terminal:

```bash
celery -A config worker -l info
```

## Docker usage

1. Copy `.env.example` to `.env`.
2. Build and start the stack:

```bash
docker compose up --build
```

Docker Compose overrides `DATABASE_URL` and `REDIS_URL` internally, so the same `.env` works for both local `venv` runs and container runs.

Services included:

- `postgres`
- `redis`
- `web`
- `celery`
- `nginx`

The site is exposed on `http://localhost:8000`.

## Environment variables

Main variables:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`
- `REDIS_URL`
- `DEFAULT_FROM_EMAIL`
- `SITE_URL`
- `USE_S3`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_STORAGE_BUCKET_NAME`
- `AWS_S3_ENDPOINT_URL`
- `AWS_S3_REGION_NAME`
- `GUNICORN_WORKERS`
- `CELERY_TASK_ALWAYS_EAGER`

See [.env.example](/home/joce/autopazar/.env.example) for defaults.

## Management commands

- `python manage.py seed_demo_data`
- `python manage.py sync_reference_data`
- `./scripts/bootstrap_demo.sh`

Quick command list:

- [docs/commands/autopazar_commands.txt](/home/joce/autopazar/docs/commands/autopazar_commands.txt)

This seeds:

- All 34 official cities/towns in North Macedonia
- A broad car brand and model catalog for the marketplace
- Demo users
- Sample listings
- Favorites
- A sample inquiry

## Tests

Run the test suite with:

```bash
pytest
```

Current coverage includes:

- Registration and login
- Listing edit permissions and status changes
- Listing filters
- Favorite toggle flow
- Inquiry form behavior
- Reporting and audit logging

## Linting and formatting

```bash
black .
isort .
flake8 .
```

## API overview

Base path: `/api/`

- `POST /api/auth/token/`
- `GET /api/users/me/`
- `PATCH /api/users/me/`
- `GET /api/users/sellers/<id>/`
- `GET /api/listings/`
- `GET /api/listings/<slug>/`
- `GET|POST|DELETE /api/favorites/`
- `GET|POST /api/messages/`
- `GET|POST /api/reports/`

## Deployment overview

Recommended VPS flow on Ubuntu:

1. Install Docker Engine and Docker Compose plugin.
2. Clone the repository and create `.env`.
3. Set `DJANGO_SETTINGS_MODULE=config.settings.production`.
4. Use a real `SECRET_KEY`, domain-based `ALLOWED_HOSTS`, and HTTPS-aware `CSRF_TRUSTED_ORIGINS`.
5. Point DNS to the VPS and terminate traffic through Nginx or an external reverse proxy.
6. Use S3-compatible storage in production if you do not want local media persistence tied to the host.
7. Run `docker compose up -d --build`.

## Render deployment

This repo includes a Render Blueprint in [render.yaml](/home/joce/autopazar/render.yaml).

Render is suitable for demo/testing for this project, but free tier has important limits:

- free web services spin down when idle
- free Postgres expires after 30 days
- free Key Value does not persist data
- local uploaded media is not durable unless you enable S3-compatible storage

For step-by-step instructions, see:

- [render.md](/home/joce/autopazar/docs/deploy/render.md)

The short version:

1. Push the repo to GitHub.
2. In Render create a `Blueprint`.
3. Let Render provision the web service, Postgres, and Key Value from [render.yaml](/home/joce/autopazar/render.yaml).
4. If you want persistent car photos, set `USE_S3=True` and add your S3/R2 environment variables.
5. Run `sync_reference_data`, `seed_demo_data`, and `createsuperuser` from your local machine against the Render database.

## Production notes

- Static files are collected on container start.
- Gunicorn serves Django behind Nginx.
- Redis backs both cache and Celery broker.
- Email verification and inquiry notifications are Celery-friendly.
- Structured console logging is enabled.
- `/health/` is available for uptime checks.

## Backups

Minimum production backup strategy:

- Daily PostgreSQL dump
- Media backup to object storage or separate block volume snapshots
- Off-host retention for both database and media

## Future roadmap

The current structure is intended to support later additions without major rewrites:

- Paid featured listings
- Dealership account types
- Real-time chat
- Saved searches
- Compare listings
- Multilingual UI
- Recommendation engine
- Native mobile app
- Analytics dashboard
- Moderation AI tooling
