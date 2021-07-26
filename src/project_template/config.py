import configparser
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


config_data = configparser.ConfigParser()
config_data.read("config.ini")

DEBUG = os.environ.get("DEBUG", "true")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")
POSTGRES_DATABASE_URL = os.environ.get(
    "POSTGRES_DATABASE_URL_ENV", "postgresql://test:test@postgres/test"
).replace("://", "+asyncpg://")

SENTRY_URL = os.environ.get("SENTRY_URL_ENV", "fake")

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN_ENV", "fake")
DISCORD_BOT_COMMAND_PREFIX = config_data["discord"]["discord_bot_command_prefix"]
COGS_EXPLICIT_INCLUDE = config_data["cogs"]["explicit_include"]
COGS_EXPLICIT_EXCLUDE = config_data["cogs"]["explicit_exclude"]

if SENTRY_URL.lower().strip() != "fake":
    import sentry_sdk
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

    sentry_sdk.init(
        SENTRY_URL,
        release="0.1.0",  # TODO automate getting this.
        traces_sample_rate=1.0,
        integrations=[SqlalchemyIntegration()],
    )

engine = create_async_engine(
    POSTGRES_DATABASE_URL,
    future=True,
    echo=True,
)

async_session = sessionmaker(
    engine, autoflush=False, autocommit=False, class_=AsyncSession, expire_on_commit=False
)


"""
General:
    - Permission to record data

Insight and Analytics:
    - Invite tracking
    - Voice activity tracking
    - Text chat activity tracking
    - Time-zone and region tracking
    - Some people will want a way to make some of this data anonymous.
    - Message spell/grammar checking (use LanguageTool API/package)

Moderation:
    - moderation features

Activity Encouragement:
    - Time Zones
    - Pinging to hang out in VC
    - Reply to message to add to a pinned single comment. used for suggestions to keep them
        organized

Group Project:
    - GitHub Integration
    - Project Team Tracking
    - Running list of active projects
"""
