import asyncio

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, StateFilter, CommandObject
from aiogram.fsm.context import FSMContext

from database.requests import rq_user
from database.requests import rq_token
from utils.error_handling import error_handler
from filter.admin_filter import check_super_admin
from config_data.config import Config, load_config
from anketa_question.questions import dict_questions
from handlers.anketa_handlers import Question
from keyboards.anketa_keyboard import keyboard_anketa
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
    if await check_super_admin(telegram_id=message.from_user.id):
        data = {"tg_id": tg_id, "username": username, "role": rq_user.UserRole.admin}
    await rq_user.add_user(data)
    if token:
        role = await rq_token.get_token(token=token, tg_id=message.from_user.id)
        if role:
            await rq_user.update_user_role(tg_id=message.from_user.id,
                                           role=role)
        else:
            await message.answer(text='Пригласительная ссылка не валидна')
    await message.answer(text='Привет!\n'
                              'Я рада снова видеть тебя, давай знакомиться поближе!\n\n'
                              'Я Алина Люфт— прошла путь от простого мастера до инструктора. Благодаря своему'
                              ' семилетнему опыту в подологическом и эстетическом направлениях, нашла идеальный'
                              ' тандем для безопасной эстетики.\n\n'
                              'И это - пилочный маникюр и пленки. Именно в них я влюбляю своих учеников.\n\n'
                              'Благодаря этим техникам мастера:\n\n'
                              '▫️расширяют спектр своих услуг;\n\n'
                              '▫️повышают прайс;\n\n'
                              '▫️ускоряются в 2 раза;\n\n'
                              '▫️становятся востребованными и уникальными специалистами.\n\n'
                              'Ведь клиенты сами ищут мастеров, которые делают пилочный маникюр и пленки.\n\n'
                              '⬇️Ответь на несколько вопросов и ты получишь урок по безопасному снятию пленок🎁')
    await asyncio.sleep(3)
    question_1 = dict_questions[1]
    await state.update_data(answer=[])
    if question_1['list_buttons']:

        await message.answer(text=question_1['message'],
                             reply_markup=keyboard_anketa(list_answer=question_1['list_buttons'],
                                                          count_question=1))
    else:
        await message.answer(text=question_1['message'])
        await state.set_state(Question.question)


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

