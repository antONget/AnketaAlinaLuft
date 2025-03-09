from database.models import async_session
from database.models import User
from sqlalchemy import select
from dataclasses import dataclass
import logging


""" USER """


@dataclass
class UserRole:
    user = "user"
    partner = "partner"
    admin = "admin"
    executor = "executor"


""" ADD """


async def add_user(data: dict) -> int | None:
    """
    Добавление пользователя
    :param data:
    :return:
    """
    logging.info(f'add_user')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == data['tg_id']))
        if not user:
            new_user = User(**data)
            session.add(new_user)
            await session.flush()
            id_ = new_user.id
            await session.commit()
            return id_


""" GET """


async def get_user_tg_id(tg_id: int) -> User:
    logging.info('get_user_tg_id')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def get_users_role(role: str) -> list[User]:
    """
    Получение списка пользователей с заданной ролью
    :param role:
    :return:
    """
    logging.info('get_users_role')
    async with async_session() as session:
        users = await session.scalars(select(User).where(User.role == role))
        list_users = [user for user in users]
        return list_users


async def get_user_username(username: str) -> User:
    logging.info('get_user_username')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.username == username))


async def get_users() -> list[User]:
    logging.info('get_users')
    async with async_session() as session:
        users = await session.scalars(select(User))
        users_list = [user for user in users]
        return users_list


""" UPDATE """


async def update_username(tg_id: int, username: str) -> None:
    logging.info('update_username')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.username = username
            await session.commit()


async def update_user_role(tg_id: int, role: str) -> None:
    """
    Обновление роли пользователя
    :param tg_id:
    :param role:
    :return:
    """
    logging.info('set_user_phone')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.role = role
            await session.commit()


""" DELETE """


async def delete_user_tg_id(tg_id: int) -> None:
    logging.info('delete_user_tg_id')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            await session.delete(user)
            await session.commit()
