from datetime import datetime
from sqlalchemy import select, delete, update
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Author, Banner, Category, CeramicMaster, CeramicService, CeramicWork, Event, Product


############### Working with banners (information for pages)################
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


############################## CATEGORY ######################################

async def orm_get_categories(session: AsyncSession):
    query = select(Category)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_category_by_name(session: AsyncSession, name: str):
    query = select(Category).where(Category.name == name)
    result = await session.execute(query)
    return result.scalar()


async def orm_create_categories(session: AsyncSession, categories: list):
    query = select(Category)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Category(name=name) for name in categories])
    await session.commit()


############################### AUTHOR #######################################

async def orm_create_author(session: AsyncSession, author_info: dict):
    obj = Author(
        name=author_info["name"],
        telegram_id=int(author_info["telegram_id"]),
        category=int(author_info["category"]),
    )
    session.add(obj)
    await session.commit()


async def orm_get_authors(session: AsyncSession):
    query = select(Author)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_authors_by_category(session: AsyncSession, category: int):
    query = select(Author).where(Author.category == category)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_authors_by_name(session: AsyncSession, name: str):
    query = select(Author).where(Author.name == name)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_authors_by_id(session: AsyncSession, id: int):
    query = select(Author).where(Author.id == id)
    result = await session.execute(query)
    return result.scalar()


async def orm_delete_author(session: AsyncSession, id: int):
    query = delete(Author).where(Author.id == id)
    await session.execute(query)
    await session.commit()


############################ EVENT ######################################
async def orm_create_event(session: AsyncSession, event_info: dict):
    date = datetime.strptime(event_info["date"], '%d.%m.%Y')
    obj = Event(
        title=event_info["title"],
        description=event_info["description"],
        image=event_info["image"],
        date=date,
        category=int(event_info["category"]),
        author=int(event_info["author"]),
    )
    session.add(obj)
    await session.commit()


async def orm_get_events(session: AsyncSession): # TODO
    query = select(Event)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_events_by_category(session: AsyncSession, category: int):
    query = select(Event).where(Event.category == category)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_events_by_category_and_date(
        session: AsyncSession, category: int
    ):
    query = (
        select(Event).where(Event.category == category)
        .filter(Event.date > datetime.now())
        .order_by(Event.date)
    )
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_event_by_title(session: AsyncSession, title: str): # TODO
    query = select(Event).where(Event.title == title)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_event_by_id(session: AsyncSession, id: int):
    query = (
        select(Event).where(Event.id == id)
        .options(joinedload(Event.authors))
        .options(joinedload(Event.categorys))
    )
    result = await session.execute(query)
    return result.unique().scalar()


async def orm_get_event_by_year(session: AsyncSession, date: datetime):
    start_time = datetime(date.year, 1, 1)
    end_time = datetime(date.year, 12, 31)
    print(start_time, end_time)
    print("!!!!!!!!!!!!!!!!!!!!!!!")
    query = (
        select(Event).filter(Event.date >= start_time, Event.date <= end_time)
        .options(joinedload(Event.authors))
        .options(joinedload(Event.categorys))
    )
    result = await session.execute(query)
    return result.unique().scalars().all()


async def orm_delete_event(session: AsyncSession, id: int):
    query = delete(Event).where(Event.id == id)
    await session.execute(query)
    await session.commit()


############################ PRODUCT ######################################
async def orm_create_product(session: AsyncSession, product_info: dict):
    obj = Product(
        name=product_info["name"],
        description=product_info["description"],
        price=int(product_info["price"]),
        image=product_info["image"],
        category=int(product_info["category"]),
        author=int(product_info["author"]),
        status=(product_info["status"]).upper(),
    )
    session.add(obj)
    await session.commit()


async def orm_get_products_by_category(session: AsyncSession, category: int):
    query = (
        select(Product).where(Product.category == category)
        .options(joinedload(Product.author_product))
        .options(joinedload(Product.product_category))
    )
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_products_by_author_and_category(
        session: AsyncSession, category: int, author: int
    ):
    query = (
        select(Product).where(Product.category == category)
        .filter(Product.author == author)
        .options(joinedload(Product.author_product))
        .options(joinedload(Product.product_category))
    )
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_product_by_id(session: AsyncSession, id: int):
    query = (
        select(Product).where(Product.id == id)
        .options(joinedload(Product.author_product))
    )
    result = await session.execute(query)
    return result.unique().scalar()


async def orm_get_products_by_type_and_category(
        session: AsyncSession, category: int, type: str
    ):
    query = (
        select(Product).where(
            Product.category == category, Product.status == type
        )
        .options(joinedload(Product.author_product))
        .options(joinedload(Product.product_category))
    )
    result = await session.execute(query)
    return result.scalars().all()


async def orm_delete_product(session: AsyncSession, id: int):
    query = delete(Product).where(Product.id == id)
    await session.execute(query)
    await session.commit()
# _______________________________________________________



# async def orm_get_ceramic_master(session: AsyncSession, author_id: int):
#     query = select(Author).where(Author.id == author_id)
#     result = await session.execute(query)
#     return result.scalar()


# async def orm_delete_ceramic_master(session: AsyncSession, author_id: int):
#     query = delete(Author).where(Author.id == author_id)
#     await session.execute(query)
#     await session.commit()


# # Раздел керамики: Мастера
# async def orm_add_ceramic_master(session: AsyncSession, name: str):
#     obj = CeramicMaster(
#         name=name,
#     )
#     session.add(obj)
#     await session.commit()


# async def orm_get_ceramic_masters(session: AsyncSession):
#     query = select(CeramicMaster)
#     result = await session.execute(query)
#     return result.scalars().all()


# async def orm_get_ceramic_master(session: AsyncSession, master_id: int):
#     query = select(CeramicMaster).where(CeramicMaster.id == master_id)
#     result = await session.execute(query)
#     return result.scalar()


# async def orm_delete_ceramic_master(session: AsyncSession, master_id: int):
#     query = delete(CeramicMaster).where(CeramicMaster.id == master_id)
#     await session.execute(query)
#     await session.commit()


# # Раздел керамики: Сервисы
# async def orm_add_ceramic_service(session: AsyncSession, name: str, price: int):
#     obj = CeramicService(
#         title=name,
#         price=price
#     )
#     session.add(obj)
#     await session.commit()


# async def orm_get_ceramic_services(session: AsyncSession):
#     query = select(CeramicService)
#     result = await session.execute(query)
#     return result.scalars().all()


# async def orm_get_ceramic_service(session: AsyncSession, service_id: int):
#     query = select(CeramicService).where(CeramicService.id == service_id)
#     result = await session.execute(query)
#     return result.scalar()


# async def orm_delete_ceramic_service(session: AsyncSession, service_id: int):
#     query = delete(CeramicService).where(CeramicService.id == service_id)
#     await session.execute(query)
#     await session.commit()


# # Раздел керамики: Работы
# async def orm_add_ceramic_work(
#         session: AsyncSession,
#         title: str,
#         description: str,
#         price: int,
#         master_id: int
#     ):
#     obj = CeramicWork(
#         title=title,
#         description=description,
#         price=price,
#         master=master_id
#     )
#     session.add(obj)
#     await session.commit()


# # async def orm_get_ceramic_works(session: AsyncSession):
# #     query = select(CeramicWork)
# #     result = await session.execute(query)
# #     return result.scalars().all()


# async def orm_get_ceramic_works_by_master(
#         session: AsyncSession, master_id: int
#     ):
#     query = select(CeramicWork).where(CeramicWork.master == master_id)
#     result = await session.execute(query)
#     return result.scalars().all()


# async def orm_get_ceramic_work(session: AsyncSession, work_id: int):
#     query = select(CeramicWork).where(CeramicWork.id == work_id)
#     result = await session.execute(query)
#     return result.scalar()


# async def orm_get_ceramic_works(session: AsyncSession):
#     query = select(CeramicWork)
#     result = await session.execute(query)
#     return result.scalars().all()



# async def orm_delete_ceramic_work(session: AsyncSession, work_id: int):
#     query = delete(CeramicWork).where(CeramicWork.id == work_id)
#     await session.execute(query)
#     await session.commit()
