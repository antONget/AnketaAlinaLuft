import logging

from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command


from config_data.config import Config, load_config

router = Router()
config: Config = load_config()


@router.message(Command('help'))
async def command_help(message: Message, bot: Bot) -> None:
    """
    Помощь
    :param message:
    :param bot:
    :return:
    """
    logging.info('command_help')
    await message.answer(text='это текстовый месcедж про цену/цены')


@router.message(Command('support'))
async def command_support(message: Message, bot: Bot) -> None:
    """
    Поддержка
    :param message:
    :param bot:
    :return:
    """
    logging.info('command_support')
    await message.answer(text=f'Если у вас возникли вопросы по работе бота, сложности при оплате заказа или есть'
                              f' предложения по улучшению функционала напишите мне {config.tg_bot.manager}')