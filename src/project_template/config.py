import os


DEBUG = os.environ.get("DEBUG", "true")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")
POSTGRES_DATABASE_URL = os.environ.get(
    "POSTGRES_DATABASE_URL_ENV", "postgresql://test:test@postgres/test"
)

SENTRY_URL = os.environ.get("SENTRY_URL_ENV", "fake")

if SENTRY_URL.lower().strip() != "fake":
    import sentry_sdk
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

    sentry_sdk.init(
        SENTRY_URL,
        release="0.1.0",  # TODO automate getting this.
        traces_sample_rate=1.0,
        integrations=[SqlalchemyIntegration()],
    )
