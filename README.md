# FastAPI SaaS Boilerplate

A small FastAPI starting point for a SaaS API. It includes application settings,
an async SQLModel database setup, JWT/password helpers, and early authentication
and Stripe billing modules. Docker, Railway, and Procfile deployment definitions
are included.

> **Project status:** the currently running application exposes only the root and
> health routes. Authentication and billing endpoint modules exist in the source,
> but their router is empty and is not included by `app/main.py`. Database migration
> version files are also not present. This README describes the repository as it is
> today, rather than treating those modules as completed, public API features.

## What runs now

| Route | Purpose |
| --- | --- |
| `GET /` | Returns a simple active-service response. |
| `GET /health` | Returns `{"status": "healthy"}` for platform health checks. |
| `GET /docs` | Swagger UI. |
| `GET /redoc` | ReDoc API reference. |
| `GET /api/v1/openapi.json` | OpenAPI document used by the documentation UIs. |

## Requirements

- Python 3.11 or newer
- `pip`
- Values for `DATABASE_URL`, `REDIS_URL`, and `SECRET_KEY` (they are required
  application settings, even though the active root and health routes do not use
  the database or Redis)

PostgreSQL and Redis are needed once the data-backed modules are connected and
used. A local service is not required merely to start the currently exposed
routes.

## Run locally

```bash
git clone <your-repository-url>
cd fastapi-saas-boilerplate

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
```

Update `.env` with local development values. The included values illustrate the
expected format; do not use the sample secret in a deployed environment.

```dotenv
PROJECT_NAME="FastAPI SaaS Boilerplate"
DATABASE_URL="postgresql://postgres:password@localhost:5432/db"
REDIS_URL="redis://localhost:6379/0"
SECRET_KEY="replace-with-a-long-random-secret"
STRIPE_API_KEY=""
STRIPE_WEBHOOK_SECRET=""
```

Start the development server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open [http://localhost:8000/docs](http://localhost:8000/docs), or check the
service directly:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"healthy"}
```

## Configuration

Settings are loaded from environment variables and, for local development, from
`.env`. See [`.env.example`](.env.example) for the starting template.

| Variable | Required | Default | Notes |
| --- | :---: | --- | --- |
| `PROJECT_NAME` | No | `FastAPI SaaS Boilerplate` | API title shown in docs. |
| `API_V1_STR` | No | `/api/v1` | Prefix used for the OpenAPI JSON URL. |
| `DATABASE_URL` | Yes | — | PostgreSQL URL. The async engine changes a `postgres://` prefix to `postgresql+asyncpg://`. |
| `REDIS_URL` | Yes | — | Reserved for Redis integration; no client is currently created. |
| `SECRET_KEY` | Yes | — | Key used to sign JWTs. Use a long random value in every environment. |
| `ALGORITHM` | No | `HS256` | JWT signing algorithm. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `30` | Default JWT lifetime. |
| `STRIPE_API_KEY` | No | empty string | Stripe secret API key, used by the Stripe service module. |

`STRIPE_WEBHOOK_SECRET` is present in `.env.example` and read by the billing
endpoint module, but it is not currently declared in `Settings`. Add it to
`app/core/config.py` before enabling the webhook route.

## Repository layout

```text
.
├── app/
│   ├── main.py                 # FastAPI application; root and health routes
│   ├── api/v1/
│   │   ├── router.py           # Empty router aggregation module
│   │   └── endpoints/
│   │       ├── auth.py         # Unmounted signup/login handlers
│   │       ├── billing.py      # Unmounted Stripe checkout/webhook handlers
│   │       └── users.py        # Placeholder
│   ├── core/
│   │   ├── config.py           # Environment settings
│   │   ├── database.py         # Async SQLAlchemy/SQLModel session dependency
│   │   └── security.py         # bcrypt and JWT helpers
│   ├── models/user.py          # User SQLModel table and request/response models
│   └── services/stripe.py      # Stripe Checkout and customer-portal wrappers
├── alembic/env.py              # Async migration environment
├── Dockerfile                  # Python 3.11 container build
├── Procfile                    # Process command for compatible hosts
├── railway.json                # Railway build/deploy settings
├── requirements.txt            # Python dependencies
└── .env.example                # Environment-variable template
```

## Modules prepared for integration

### Authentication

`app/api/v1/endpoints/auth.py` contains handlers intended for:

- `POST /signup` — creates a user after checking email uniqueness.
- `POST /login` — accepts OAuth2 form data (`username` is the email) and returns
  a bearer JWT.

The handlers use `User`, bcrypt password hashing, and JWT helpers. They are not
registered with the application, so these paths do not appear in `/docs` and
cannot be called until the API router is implemented and included in `main.py`.

### Billing

`app/api/v1/endpoints/billing.py` and `app/services/stripe.py` provide starter
code for subscription Checkout sessions and webhook signature verification.
They are likewise unmounted. The webhook contains only placeholder comments for
persisting subscription state, and checkout success/cancel URLs are hard-coded
examples. Treat this as integration scaffolding, not finished billing logic.

## Database and migrations

The project defines an async engine/session dependency in
`app/core/database.py`, and the `User` table is exposed to Alembic metadata in
`alembic/env.py`. There are currently no migration revision files and
`alembic.ini` lacks the usual `script_location` configuration. Consequently,
`alembic upgrade head` is not a working setup step yet.

Before using database-backed routes or the supplied production startup commands:

1. Configure Alembic's script location and create an initial migration.
2. Implement and mount the versioned API router.
3. Add tests for registration, login, protected access, Stripe verification, and
   subscription persistence.
4. Confirm the migration command against a real PostgreSQL database.

## Deployment notes

The `Dockerfile`, `Procfile`, and `railway.json` all currently run this command
before starting Uvicorn:

```bash
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
```

Because migrations are not configured completely, these deployment entry points
will fail until the database/migration work above is completed. For a deployment
of the current root and health endpoints, use a start command that runs Uvicorn
directly, provide the three required settings, and set the platform health check
to `/health`.

After migrations are established, use a production PostgreSQL URL, managed Redis
if the application begins using it, unique production secrets, and Stripe live
credentials only in the production environment. Never commit `.env` or API keys.

## Verification

After changing the project, basic checks are:

```bash
python -m compileall -q app alembic
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

In another terminal, confirm `curl http://127.0.0.1:8000/health` and inspect
`/docs`. The generated OpenAPI document is the source of truth for the routes
that are actually mounted.

## License

This project is licensed under the [MIT License](LICENSE).
