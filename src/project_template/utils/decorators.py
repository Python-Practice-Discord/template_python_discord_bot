import functools
import inspect
from typing import Optional

import discord
from discord.ext import commands
from packaging import version
from sqlalchemy.ext.asyncio import AsyncSession

from project_template.config import async_session
from project_template.utils.exceptions import UserHasNotAcceptedTOS
from project_template.utils.logger import log


__all__ = ["Session", "TOS"]


def Session(func):
    """
    Decorator that adds a SQLAlchemy AsyncSession to the function passed if the function is not
    already being passed an AsyncSession object.

    If no AsyncSession object is being passes this decorator will handle all session commit and
    rollback operations. Commit if no errors, rollback if there is an error raised.

    Example:

    @Session
    async def example(session: AsyncSession, other_data: str):
        ...

    a = await example(other_data="stuff")
    b = await example(async_session(), "stuff")


    NOTE: The FIRST argument is "session". "session" in ANY OTHER ARGUMENT SPOT will break!
    ONLY pass an AsyncSession object or NOTHING to the "session" argument!
    """

    @functools.wraps(func)
    async def wrapper_events(*args, **kwargs):
        func_mod_and_name = f"{func.__module__}.{func.__name__}"
        log.info(f"Starting {func_mod_and_name}")
        session_passed = False

        for arg in list(args) + list(kwargs.values()):
            if issubclass(type(arg), AsyncSession):
                session_passed = True
                break

        try:
            if session_passed is True:
                func_return = await func(*args, **kwargs)
            else:
                session: AsyncSession
                async with async_session() as session:
                    async with session.begin():
                        if "session" in kwargs:
                            kwargs["session"] = session
                        elif list(inspect.signature(func).parameters.keys())[0] == "session":
                            args = (session, *args)
                        else:
                            raise RuntimeError("session is not the first argument in the function")
                        func_return = await func(*args, **kwargs)

            log.info(f"Finished {func_mod_and_name}")
            return func_return
        except Exception as e:
            log.exception(e)
            raise

    return wrapper_events


def TOS(min_tos_version: Optional[str] = None):
    """
    Decorator that ensures the user calling the command or listener has accepted the correct version
    of the TOS.
    """
    from project_template.utils.database import get_user_tos_version

    def _decorator(func):
        @functools.wraps(func)
        async def wrapper_events(*args, **kwargs):
            if min_tos_version is not None:

                user_discord_id = None

                for arg in list(args) + list(kwargs.values()):
                    if issubclass(type(arg), commands.Context):
                        arg: commands.Context
                        user_discord_id = arg.author.id
                        break
                    elif issubclass(type(arg), discord.RawReactionActionEvent):
                        arg: discord.RawReactionActionEvent
                        user_discord_id = arg.user_id
                        break

                if user_discord_id is None:
                    raise ValueError("No discord_id found in function args/kwargs")

                user_accepted_tos_version = await get_user_tos_version(user_discord_id)

                if user_accepted_tos_version is None:
                    raise UserHasNotAcceptedTOS("User has not accepted the TOS")

                user_version = version.parse(user_accepted_tos_version)
                min_version = version.parse(min_tos_version)

                if min_version > user_version:
                    raise UserHasNotAcceptedTOS(
                        f"Min TOS version accepted {min_version} is less "
                        f"than the current TOS version {user_version}"
                    )
            return await func(*args, **kwargs)

        return wrapper_events

    return _decorator
