from discord.ext.commands import Context
from sqlalchemy import select

from project_template import schema
from project_template.utils.decorators import Session


@Session
async def accepted_tos(session, ctx: Context) -> bool:
    user_tos = await session.execute(
        select(schema.UserPrivacyTOS.user_id)
        .join(schema.User, schema.User.id == schema.UserPrivacyTOS.user_id)
        .filter(schema.User.id == ctx.author.id)
    ).all()
    # TODO check TOS version
    # TODO maybe have some things work for some TOS versions and not others?

    return len(user_tos) >= 1
