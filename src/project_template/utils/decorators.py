import functools

from sqlalchemy.ext.asyncio import AsyncSession

from project_template.config import async_session
from project_template.utils.logger import log


__all__ = ["Session"]


def Session(func):
    @functools.wraps(func)
    async def wrapper_events(*args, **kwargs):
        func_mod_and_name = f"{func.__module__}.{func.__name__}"
        log.info(f"Starting {func_mod_and_name}")
        session_passed = False
        try:
            try:
                if isinstance(args[0], AsyncSession):
                    session_passed = True
            except IndexError:
                pass

            if session_passed is True:
                func_return = await func(*args, **kwargs)
            else:
                async with async_session() as session:
                    async with session.begin():
                        args = (session, *args)
                        func_return = await func(*args, **kwargs)
        except Exception as e:
            log.exception(e)
            raise
        log.info(f"Finished {func_mod_and_name}")
        return func_return

    return wrapper_events
