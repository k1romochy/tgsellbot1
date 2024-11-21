from typing import cast

from sqlalchemy.orm import selectinload

from core.models.user import User
import core.models.db_helper as db
from sqlalchemy.engine import Result
from sqlalchemy import select


async def create_user(tg_id: int) -> None:
    async with db.async_session() as session:
        user: User = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
