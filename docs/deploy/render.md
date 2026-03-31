# Render Deployment

This project can run on Render free tier for demo/testing, but there are important tradeoffs:

- free web services spin down after inactivity
- free Postgres expires after 30 days
- free Key Value does not persist data to disk
- local `/media` storage is not durable on Render

For a proper demo with car images that survive redeploys, enable `USE_S3=True` and use S3-compatible object storage such as Cloudflare R2, AWS S3, or DigitalOcean Spaces.

## Recommended setup

Use the root [render.yaml](/home/joce/autopazar/render.yaml) Blueprint:

- `autopazar-web`
- `autopazar-db`
- `autopazar-redis`

Current free-tier behavior:

- Django web service runs on Render
- Postgres is managed by Render
- Redis-compatible Key Value is managed by Render
- Celery tasks run inline via `CELERY_TASK_ALWAYS_EAGER=true`
- email defaults to console backend unless you configure SMTP

## Create the Blueprint

1. Push the latest code to GitHub.
2. In Render, click `New` -> `Blueprint`.
3. Connect the repository.
4. Render will detect [render.yaml](/home/joce/autopazar/render.yaml).
5. Create the resources.

## Persistent media with S3 or R2

Set these environment variables on the `autopazar-web` service:

```text
USE_S3=True
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...
AWS_S3_ENDPOINT_URL=...
AWS_S3_REGION_NAME=...
AWS_S3_CUSTOM_DOMAIN=
AWS_S3_ADDRESSING_STYLE=
AWS_QUERYSTRING_AUTH=False
AWS_S3_FILE_OVERWRITE=False
```

### Cloudflare R2 example

Typical R2 values:

```text
USE_S3=True
AWS_ACCESS_KEY_ID=<R2 access key>
AWS_SECRET_ACCESS_KEY=<R2 secret key>
AWS_STORAGE_BUCKET_NAME=<bucket name>
AWS_S3_ENDPOINT_URL=https://<accountid>.r2.cloudflarestorage.com
AWS_S3_REGION_NAME=auto
AWS_S3_CUSTOM_DOMAIN=
AWS_S3_ADDRESSING_STYLE=path
AWS_QUERYSTRING_AUTH=False
AWS_S3_FILE_OVERWRITE=False
```

If you create a public custom domain for the bucket, set `AWS_S3_CUSTOM_DOMAIN` to that hostname.

## First-time remote setup

Free Render web services do not provide shell / one-off jobs, so run the initial data load from your own machine against the Render database:

```bash
cd /home/joce/autopazar
source .venv/bin/activate
export DJANGO_SETTINGS_MODULE=config.settings.production
export DATABASE_URL='<render external database url>'
export REDIS_URL='<render key value url>'
export SECRET_KEY='<same value as Render web service>'
python manage.py sync_reference_data
python manage.py seed_demo_data
python manage.py createsuperuser
```

## Health check

After deploy, open:

```text
https://<your-render-service>.onrender.com/health/
```

You should receive:

```json
{"status": "ok"}
```
