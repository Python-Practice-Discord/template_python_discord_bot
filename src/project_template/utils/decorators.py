import asyncio
import functools
import inspect

from sqlalchemy.ext.asyncio import AsyncSession

from project_template.config import async_session
from project_template.utils.logger import log


__all__ = ["Session"]


def Session(func):
    """
    Decorator that adds a SQLalchemy AsyncSession to the function passed if the function is not
    already being passed an AsyncSession object.
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
            if isinstance(arg, AsyncSession):
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


async def call_():
    await _test("other", "something")


@Session
async def _test(session, other, something=False):
    pass


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(call_())
