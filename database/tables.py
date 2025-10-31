from datetime import date, datetime

from sqlalchemy import String, BigInteger, Date, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(900))
    tg_username: Mapped[str] = mapped_column(String(900), nullable=True)
    register_date: Mapped[date] = mapped_column(Date, default=date.today())
    balance: Mapped[int] = mapped_column(BigInteger, default=0)
    requests: Mapped[int] = mapped_column(BigInteger, default=0)

    task = relationship('Task', back_populates='user')


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(900))
    event_type: Mapped[str] = mapped_column(String(900), nullable=True)
    event_date: Mapped[date] = mapped_column(Date)
    reminder: Mapped[datetime] = mapped_column(DateTime)
    description: Mapped[str] = mapped_column(String(4000), nullable=True)

    user = relationship('User', back_populates='task')

    def as_kwargs(self):
        return {
            'task_id': self.id,
            'user_name': self.user.name,
            'name': self.name,
            'event': self.event_type,
            'date': self.event_date,
            'reminder': self.reminder,
        }
