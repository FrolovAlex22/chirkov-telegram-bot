from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import BigInteger, ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class StatusProduct(PyEnum):
    PRODUCT = "product"
    SERVICE = "service"


class Base(DeclarativeBase):
    __abstract__ = True
    # created_at: Mapped[datetime] = mapped_column(
    #     index=True,
    #     server_default=func.now()
    # )


class Banner(Base):
    __tablename__ = "banner"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    image: Mapped[str] = mapped_column(String(150), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    category: Mapped[int] = mapped_column(
        ForeignKey("category.id"), nullable=False
    )


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str] = mapped_column(String(150), nullable=True)
    date: Mapped[datetime] = mapped_column(nullable=True)
    category: Mapped[int] = mapped_column(
        ForeignKey("category.id", ondelete="SET NULL"), nullable=True
    )
    author: Mapped[int] = mapped_column(
        ForeignKey("author.id", ondelete="SET NULL"), nullable=True
    )
    authors: Mapped["Author"] = relationship(backref="authors")
    categorys: Mapped["Category"] = relationship(
        backref="categorys"
    )


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[int] = mapped_column(nullable=True)
    image: Mapped[str] = mapped_column(String(150), nullable=True)
    category: Mapped[int] = mapped_column(
        ForeignKey("category.id", ondelete="SET NULL"), nullable=True
    )
    author: Mapped[int] = mapped_column(
        ForeignKey("author.id", ondelete="SET NULL"), nullable=True,
    )
    status: Mapped[StatusProduct] = mapped_column(
        default=StatusProduct.PRODUCT,
        server_default="PRODUCT",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        index=True,
        server_default=func.now()
    )
    author_product: Mapped["Author"] = relationship(
        backref="author_product"
    )
    product_category: Mapped["Category"] = relationship(
        backref="product_category"
    )


class CeramicMaster(Base):
    __tablename__ = "cermic_master"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)


class CeramicService(Base):
    __tablename__ = "cermic_service"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)


class CeramicWork(Base):
    __tablename__ = "cermic_work"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    master: Mapped[int] = mapped_column(
        ForeignKey("cermic_master.id"), nullable=False
    )
