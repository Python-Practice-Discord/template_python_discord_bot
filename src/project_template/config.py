import configparser
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


VERSION = ("0.1.0",)  # TODO automate getting this.
SENTRY_URL = os.environ.get("SENTRY_URL_ENV", "fake")
if SENTRY_URL.lower().strip() != "fake":
    import sentry_sdk
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

    sentry_sdk.init(
        SENTRY_URL,
        release=VERSION,
        traces_sample_rate=1.0,
        integrations=[SqlalchemyIntegration()],
    )

config_data = configparser.ConfigParser()
config_data.read("config.ini")

DEBUG = os.environ.get("DEBUG", "true")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")
POSTGRES_DATABASE_URL = os.environ.get(
    "POSTGRES_DATABASE_URL_ENV", "postgresql://test:test@postgres/test"
).replace("://", "+asyncpg://")

BOT_NAME = config_data["discord"]["bot_name"]
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN_ENV", "fake")
DISCORD_BOT_COMMAND_PREFIX = config_data["discord"]["bot_command_prefix"]
DISCORD_TOS_CHANNEL_ID: str = ""  # This is set in main.py
DISCORD_BOT_CHANNEL_ID: str = ""  # This is set in main.py
COGS_EXPLICIT_INCLUDE = config_data["cogs"]["explicit_include"]
COGS_EXPLICIT_EXCLUDE = config_data["cogs"]["explicit_exclude"]

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
