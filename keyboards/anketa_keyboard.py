import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard_anketa(list_answer: list[str], count_question: int) -> InlineKeyboardMarkup:
    """
    Клавиатура для ответа на вопросы
    :param list_answer:
    :param count_question:
    :return:
    """
    button = []
    for answer in list_answer:
        button.append([InlineKeyboardButton(text=answer, callback_data=f'question_{answer}_{count_question}')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)
    return keyboard
