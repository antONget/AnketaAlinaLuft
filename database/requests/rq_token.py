from database.models import async_session
from database.models import Token
from sqlalchemy import select

import logging


""" TOKEN """


async def add_token(data: dict) -> None:
    """
    Добавление токена
    :param data:
    :return:
    """
    logging.info(f'add_token')
    async with async_session() as session:
        new_token = Token(**data)
        session.add(new_token)
        await session.commit()


async def get_token(token: str, tg_id: int) -> bool | str:
    """
    Проверка валидности токена
    :param token:
    :param tg_id:
    :return:
    """
    logging.info('get_token')
    async with async_session() as session:
        token_ = await session.scalar(select(Token).filter(Token.token == token,
                                                           Token.tg_id == 0))
        if token_:
            token_.tg_id = tg_id
            role = token_.role
            await session.commit()
            return role
        else:
            return False
