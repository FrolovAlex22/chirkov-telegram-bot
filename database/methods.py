from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Channel


# # Каналы
# async def orm_add_channel(session: AsyncSession, data: dict):
#     obj = Channel(
#         name=data["name"],
#     )
#     session.add(obj)
#     await session.commit()


# async def orm_get_channels(session: AsyncSession):
#     query = select(Channel)
#     result = await session.execute(query)
#     return result.scalars().all()


# async def orm_get_channel(session: AsyncSession, channel_id: int):
#     query = select(Channel).where(Channel.id == channel_id)
#     result = await session.execute(query)
#     return result.scalar()


# async def orm_delete_channel(session: AsyncSession, channel_id: int):
#     query = delete(Channel).where(Channel.id == channel_id)
#     await session.execute(query)
#     await session.commit()
