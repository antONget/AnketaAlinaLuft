from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from utils.error_handling import error_handler
from config_data.config import Config, load_config
from anketa_question.questions import dict_questions
from keyboards.anketa_keyboard import keyboard_anketa
from utils.send_admins import send_text_admins

import logging

router = Router()
router.message.filter(F.chat.type == "private")
config: Config = load_config()


class Question(StatesGroup):
    question = State()


@router.message(F.text, StateFilter(Question.question))
@error_handler
async def get_answer_question(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Получаем ответ на вопрос
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_answer_question ')
    data = await state.get_data()
    answer = data['answer']
    if len(dict_questions) < len(answer):
        data = await state.get_data()
        answer = data['answer']
        answer.append(message.text)
        text = f'Пользователь <a href="tg://userid?id={message.from_user.id}">{message.from_user.username}</a> ' \
               f'ответил на вопросы анкеты:\n\n'
        for k, v in dict_questions.items():
            text += f'<b>{k}. {v["message"]}</b>\n{answer[k - 1]}\n\n'
        await send_text_admins(bot=bot, text=text)
    answer.append(message.text)
    await state.update_data(answer=answer)
    count_question = len(answer) + 1
    if len(dict_questions) < count_question:
        pass
    else:
        questions = dict_questions[count_question]
        if questions['list_buttons']:
            try:
                await message.edit_text(text=questions['message'],
                                        reply_markup=keyboard_anketa(list_answer=questions['list_buttons'],
                                                                     count_question=count_question))
            except:
                await message.answer(text=questions['message'],
                                     reply_markup=keyboard_anketa(list_answer=questions['list_buttons'],
                                                                  count_question=count_question))
            await state.set_state(state=None)
        else:
            await message.answer(text=questions['message'])
            await state.set_state(Question.question)
            await state.update_data(answer=count_question)


@router.callback_query(F.data.startswith('question'))
async def process_select_answer(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Возврат в начало бота
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_select_answer ')
    count_question = int(callback.data.split('_')[-1]) + 1
    if len(dict_questions) < count_question:
        await callback.message.answer_video(
            video='BAACAgIAAxkBAAMSZ9Bs7k2pJyHq_bhxcw1hiGqkAusAAmplAALbM4BKCwKZkLwTRzo2BA',
            caption='🎁Урок «Безопасное снятие плёнок»')
        data = await state.get_data()
        answer = data['answer']
        answer.append(callback.data.split('_')[-2])
        text = f'Пользователь <a href="tg://user?id={callback.from_user.id}">{callback.from_user.username}</a> ' \
               f'ответил на вопросы анкеты:\n\n'
        for k, v in dict_questions.items():
            text += f'<b>{k}. {v["message"]}</b>\n{answer[k-1]}\n\n'
        await send_text_admins(bot=bot, text=text)
    else:
        data = await state.get_data()
        answer = data['answer']
        answer.append(callback.data.split('_')[-2])
        await state.update_data(answer=answer)
        questions = dict_questions[count_question]
        if questions['list_buttons']:
            try:
                await callback.message.edit_text(text=questions['message'],
                                                 reply_markup=keyboard_anketa(list_answer=questions['list_buttons'],
                                                                              count_question=count_question))
            except:
                await callback.message.answer(text=questions['message'],
                                              reply_markup=keyboard_anketa(list_answer=questions['list_buttons'],
                                                                           count_question=count_question))
        else:
            await callback.message.answer(text=questions['message'])
            await state.set_state(Question.question)
    await callback.answer()