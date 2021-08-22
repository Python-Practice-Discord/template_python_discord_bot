import configparser
import os
from enum import Enum, unique
from typing import Set, Union

import toml
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


_pyproject_toml = toml.load("pyproject.toml")

VERSION = _pyproject_toml["tool"]["poetry"]["version"]
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
)
if "asyncpg" not in POSTGRES_DATABASE_URL:
    POSTGRES_DATABASE_URL = POSTGRES_DATABASE_URL.replace("://", "+asyncpg://")

BOT_NAME = config_data["discord"]["bot_name"]
DISCORD_TOKEN = os.environ["DISCORD_TOKEN_ENV"]
DISCORD_BOT_COMMAND_PREFIX = config_data["discord"]["bot_command_prefix"]
DISCORD_TOS_CHANNEL_ID: str = ""  # This is set in main.py
DISCORD_BOT_CHANNEL_ID: str = ""  # This is set in main.py
COGS_EXPLICIT_INCLUDE = config_data["cogs"]["explicit_include"]
COGS_EXPLICIT_EXCLUDE = config_data["cogs"]["explicit_exclude"]


def _get_discord_roles(role_name: str) -> Set[Union[str, int]]:
    inherit_string = "*"
    roles = set()
    for role in config_data["discord.roles"][role_name].split(","):
        if role.startswith(inherit_string):
            roles.update(_get_discord_roles(role.replace(inherit_string, "")))
            continue

        role = role.strip()
        if len(role) > 0:
            try:
                roles.add(int(role))
            except ValueError:
                roles.add(role)

    return roles


@unique
class Roles(Enum):
    admin = _get_discord_roles("admin")
    mod = _get_discord_roles("mod")
    user = _get_discord_roles("user")


GIT_REPO_URL = config_data["git"]["repo_url"]
GIT_REPO_PRIVACY_URL = f"{GIT_REPO_URL}/{config_data['git']['privacy_location']}"

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

On GH PR have pr linked to channel for devs
"""
