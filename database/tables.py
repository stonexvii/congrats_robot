from datetime import date, datetime

from sqlalchemy import String, BigInteger, Date, Boolean, ForeignKey, DateTime
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

    user = relationship('Event', back_populates='event')


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(900))
    event_type: Mapped[str] = mapped_column(String(900), nullable=True)
    event_date: Mapped[date] = mapped_column(Date)
    reminder: Mapped[datetime] = mapped_column(DateTime)
    description: Mapped[str] = mapped_column(String(4000), default='Описание')

    event = relationship('User', back_populates='user')
