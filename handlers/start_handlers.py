from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, StateFilter, CommandObject
from aiogram.fsm.context import FSMContext

from database.requests import rq_user
from database.requests import rq_token
from utils.error_handling import error_handler
from keyboards.start_keyboard import keyboard_start
from filter.filter_user_role import IsRoleAdmin
from config_data.config import Config, load_config

import logging

router = Router()
router.message.filter(F.chat.type == "private")
config: Config = load_config()


class SelectTeam(StatesGroup):
    team = State()


@router.message(CommandStart())
@error_handler
async def process_press_start(message: Message, state: FSMContext, command: CommandObject, bot: Bot) -> None:
    """
    Обработка нажатия на кнопку старт и вывод списка события
    :param message:
    :param state:
    :param command:
    :param bot:
    :return:
    """
    logging.info('process_press_start ')
    token = command.args
    tg_id: int = message.from_user.id
    username: str = message.from_user.username
    data = {"tg_id": tg_id, "username": username}
    if await IsRoleAdmin():
        data = {"tg_id": tg_id, "username": username, "role": rq_user.UserRole.admin}
        await message.answer(text='Вы АДМИНИСТРАТОР проекта',
                             reply_markup=keyboard_start())
    await rq_user.add_user(data)
    if token:
        role = await rq_token.get_token(token=token, tg_id=message.from_user.id)
        if role:
            await rq_user.update_user_role(tg_id=message.from_user.id,
                                           role=role)
        else:
            await message.answer(text='Пригласительная ссылка не валидна')


@router.callback_query(F.data == 'cancel')
async def process_select_action(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Возврат в начало бота
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    await state.clear()

