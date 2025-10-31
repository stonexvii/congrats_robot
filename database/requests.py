from datetime import date, datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .db_engine import async_session, engine
from .tables import Base, User, Task


def connection(function):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            try:
                return await function(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper


async def create_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)


@connection
async def get_user(user_tg_id: int, session: AsyncSession):
    user = await session.scalar(select(User).where(User.id == user_tg_id))
    return user


@connection
async def new_user(user_tg_id: int, name: str, tg_username: str, session: AsyncSession) -> User:
    user = User(
        id=user_tg_id,
        name=name,
        tg_username=tg_username,
    )
    session.add(user)
    await session.commit()
    user = await get_user(user_tg_id)
    return user


@connection
async def update_name(user_tg_id: int, name: str, session: AsyncSession):
    stmt = update(User).where(User.id == user_tg_id).values(name=name)
    await session.execute(stmt)
    await session.commit()


@connection
async def get_task(task_id: int, session: AsyncSession):
    task = await session.scalar(select(Task).options(selectinload(Task.user)).where(Task.id == task_id))
    return task


@connection
async def new_task(user_tg_id: int, user_name: str, event_type: str, event_date: date, reminder: datetime,
                   session: AsyncSession):
    task = Task(
        user_id=user_tg_id,
        name=user_name,
        event_type=event_type,
        event_date=event_date,
        reminder=reminder,
    )
    session.add(task)
    await session.commit()
    task = await get_task(task.id)
    return task


@connection
async def get_all_tasks(session: AsyncSession):
    response = await session.scalars(
        select(Task).options(selectinload(Task.user)).where(Task.reminder > datetime.now()))
    return response.all()
