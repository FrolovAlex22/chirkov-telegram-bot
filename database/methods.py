from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Banner, CeramicMaster, CeramicService, CeramicWork


# Работа с баннерами (информационными страницами)
async def orm_add_banner_description(session: AsyncSession, data: dict):
    query = select(Banner)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all(
        [Banner(name=name, description=description) for name, description
         in data.items()]
    )
    await session.commit()


async def orm_change_banner_image(
        session: AsyncSession, name: str, image: str
):
    query = update(Banner).where(Banner.name == name).values(image=image)
    await session.execute(query)
    await session.commit()


async def orm_get_banner(session: AsyncSession, page: str):
    query = select(Banner).where(Banner.name == page)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_info_pages(session: AsyncSession):
    query = select(Banner)
    result = await session.execute(query)
    return result.scalars().all()


# Раздел керамики: Мастера
async def orm_add_ceramic_master(session: AsyncSession, name: str):
    obj = CeramicMaster(
        name=name,
    )
    session.add(obj)
    await session.commit()


async def orm_get_ceramic_masters(session: AsyncSession):
    query = select(CeramicMaster)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_ceramic_master(session: AsyncSession, master_id: int):
    query = select(CeramicMaster).where(CeramicMaster.id == master_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_delete_ceramic_master(session: AsyncSession, master_id: int):
    query = delete(CeramicMaster).where(CeramicMaster.id == master_id)
    await session.execute(query)
    await session.commit()


# Раздел керамики: Сервисы
async def orm_add_ceramic_service(session: AsyncSession, name: str, price: int):
    obj = CeramicService(
        title=name,
        price=price
    )
    session.add(obj)
    await session.commit()


async def orm_get_ceramic_services(session: AsyncSession):
    query = select(CeramicService)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_ceramic_service(session: AsyncSession, service_id: int):
    query = select(CeramicService).where(CeramicService.id == service_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_delete_ceramic_service(session: AsyncSession, service_id: int):
    query = delete(CeramicService).where(CeramicService.id == service_id)
    await session.execute(query)
    await session.commit()


# Раздел керамики: Работы
async def orm_add_ceramic_work(
        session: AsyncSession,
        title: str,
        description: str,
        price: int,
        master_id: int
    ):
    obj = CeramicWork(
        title=title,
        description=description,
        price=price,
        master=master_id
    )
    session.add(obj)
    await session.commit()


# async def orm_get_ceramic_works(session: AsyncSession):
#     query = select(CeramicWork)
#     result = await session.execute(query)
#     return result.scalars().all()


async def orm_get_ceramic_works_by_master(
        session: AsyncSession, master_id: int
    ):
    query = select(CeramicWork).where(CeramicWork.master == master_id)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_ceramic_work(session: AsyncSession, work_id: int):
    query = select(CeramicWork).where(CeramicWork.id == work_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_delete_ceramic_work(session: AsyncSession, work_id: int):
    query = delete(CeramicWork).where(CeramicWork.id == work_id)
    await session.execute(query)
    await session.commit()
