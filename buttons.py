from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from list_events import main

button_hello = KeyboardButton('Добавить информацию о собеседовании')
button_hello1 = KeyboardButton('Добавить запись собеседования')
button_hello2 = KeyboardButton("Изменить информацию о собеседовании")
hr_rev = ReplyKeyboardMarkup(resize_keyboard=True)
hr_rev.add(button_hello)
hr_rev.add(button_hello1)
hr_rev.add(button_hello2)

button_today = KeyboardButton("Сегодня")
day_but = ReplyKeyboardMarkup(resize_keyboard=True)
day_but.add(button_today)


async def get_events(hours):
    if hours is None:
        hours = 10
    print(hours)
    events = main(hours)
    events_but = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    text = []
    for event in events:
        text.append(event['summary'])
        events_but.add(KeyboardButton(event['summary']))

    return events_but,text

button_yes_no = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_yes = KeyboardButton('Да')
button_no = KeyboardButton('Нет')
button_yes_no.add(button_yes,button_no)

async def change_parametrs_but():
    but = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    but.row(KeyboardButton('ФИО'),KeyboardButton('Навыки'),KeyboardButton('Образование'))
    but.row(KeyboardButton('Тип сотрудничества'),KeyboardButton('Опыт работы'),KeyboardButton('Уровень в структуре'))
    but.row(KeyboardButton('Уровень в hard Skils'),KeyboardButton("Уровень в soft Skils"),KeyboardButton("Общий коментарий"))
    return but