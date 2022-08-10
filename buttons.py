from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from list_events import main

button_hello = KeyboardButton('Добавить информацию о собеседовании')
button_hello1 = KeyboardButton('Добавить запись собеседования')
hr_rev = ReplyKeyboardMarkup(resize_keyboard=True)
hr_rev.add(button_hello)
hr_rev.add(button_hello1)

button_late = KeyboardButton('Вчера')
button_now = KeyboardButton('Сегодня')
hr_date = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
hr_date.add(button_late, button_now)

async def get_events():
    events = main()
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