from datetime import date

from sqlalchemy import String, BigInteger, Date, Boolean, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(900))
    tg_username: Mapped[str] = mapped_column(String(900), nullable=True)
    balance: Mapped[int] = mapped_column(BigInteger)
    requests: Mapped[int] = mapped_column(BigInteger)


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(900), default='Какой-то меню')
    button: Mapped[str] = mapped_column(String(900), nullable=True)
    description: Mapped[str] = mapped_column(String(4000), default='Описание')

    media = relationship('Media', back_populates='menu')
