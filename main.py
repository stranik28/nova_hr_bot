from cgitb import text
from importlib.metadata import metadata
from buttons import hr_rev,get_events, change_parametrs_but, day_but
from config import api
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from bd import insert_val_min,add_video, update_info
import datetime

bot = Bot(token=api)

dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

class SendRev(StatesGroup):
    #Add new note
    login = State()
    choose_date = State()
    choose_event = State()
    hard_rev = State()
    soft_rev = State()
    full_rev = State()

    #Add record
    send_video = State()
    pined_video = State()

    #Change note
    change_note = State()
    change_note_params = State()
    change_params = State()
    change_changing = State()
    change_final = State()

usernames = ["reaL_IdpNik","Artemsm67","cris_tee","foxyess2020"]

async def cmd_cancel(message: types.Message, state: FSMContext):
    if message.from_user.username in usernames:
        await SendRev.login.set()
        await message.answer("Hello "+ message.from_user.full_name, reply_markup=hr_rev)
    else:
        await message.reply("You are not allowed to use this bot", reply_markup=types.ReplyKeyboardRemove())

async def start_fn(message: types.Message):
    if message.from_user.username in usernames:
        await SendRev.login.set()
        await message.answer("Hello "+ message.from_user.full_name, reply_markup=hr_rev)
    else:
        await message.reply("You are not allowed to use this bot")

async def rev(message: types.Message, state: FSMContext):
    # print(message.text)
    if message.text == "Добавить информацию о собеседовании":
        await message.answer("Выберите дату собеседования, выберете с помощью кнопок или укажите в формате в формате день месяц через точку ex: 10.02", reply_markup=day_but)
        await SendRev.next()
        # await state.update_data(events=but1)
    elif message.text == "Добавить запись собеседования":
        but,but1 = await get_events(hours = None)
        if len(but1) == 0:
            await message.answer("Нет доступных собеседований")
            return
        await message.answer("Выберете нужное собеседование", reply_markup=but)
        await SendRev.send_video.set()
    elif message.text == "Изменить информацию о собеседовании":
        await message.answer("Укажите дату собеседования в формате день месяц через точку ex: 10.02")
        await SendRev.change_note.set()
        

async def choose_date(message: types.Message, state: FSMContext):
    if message.text == "Сегодня":
        but,but1 = await get_events(hours = None)
        if len(but1) == 0:
            await message.answer("Нет доступных собеседований")
            return
        await message.answer("Выберете нужное собеседование", reply_markup=but)
    else:
        day,month = message.text.split('.')
        today = datetime.datetime.now()
        birthday = str(day)+"/"+str(month)+"/"+str(today.year)
        two = datetime.datetime.strptime(birthday,"%d/%m/%Y")  # преобразование даты из строки в дату
        hour = (today - two).days*24+((today - two).seconds//3600)
        if (int(hour) < 0) or (int(day) <0) or (int(day) > 31) or (int(month) < 0) or (int(month) > 12):
            await message.answer("Вы ввели неверную дату")
            return
        but,but1 = await get_events(hours = hour)
        if len(but1) == 0:
            await message.answer("Нет доступных собеседований")
            return
        await state.update_data(events=but1)
        await message.answer("Выберете нужное собеседование", reply_markup=but)
    await SendRev.next()
    await state.update_data(events=but1)



async def chose_event(message: types.Message, state: FSMContext):
    but = await state.get_data()
    but = but['events']
    if message.text not in but:
        await message.answer("Используйте кнопки для выбора")
        return
    await state.update_data(sobes=message.text)
    await SendRev.next()
    await message.answer("Оцените уровень hard скилов от 0 до 10")

async def hard(message: types.Message, state: FSMContext):
    await state.update_data(hard=message.text)
    await SendRev.next()
    await message.answer("Оцените уровень soft скилов от 0 до 10")

async def soft(message: types.Message, state: FSMContext):
    await state.update_data(soft=message.text)
    await SendRev.next()
    await message.answer("Дайте общий коментарий к собеседованию")

async def full(message: types.Message, state: FSMContext):
    await state.update_data(full=message.text)
    full = await state.get_data()
    user = message.from_user.username
    save = await state.get_data()
    await state.update_data(username = user)
    save = await state.get_data()
    data = []
    data = [save['username'],save['sobes'],save['full'],save['hard'],save['soft']]
    await insert_val_min(data)
    await message.answer("Запись добавлена", reply_markup=hr_rev)
    await state.finish()
    await SendRev.login.set()

async def choose_video(message: types.Message, state: FSMContext):
    but = await state.get_data()
    but = but['events']
    if message.text not in but:
        await message.answer("Используйте кнопки для выбора")
        return
    await state.update_data(sobes=message.text)
    await message.answer("Отправьте файл")
    await SendRev.pined_video.set()

async def download_video(message, state: FSMContext):
    file_id = await bot.get_file(message.photo[-1].file_id)
    file = file_id.file_path
    await message.answer("Видео добавлено",reply_markup=hr_rev)
    # ... Saving data ...
    vid = []
    save = await state.get_data()
    vid.append(save['sobes'])
    vid.append(file_id['file_unique_id'])
    await add_video(vid)
    await state.finish()
    await SendRev.login.set()

async def change_params(message, state:FSMContext):
    day,month = message.text.split('.')
    today = datetime.datetime.now()
    birthday = str(day)+"/"+str(month)+"/"+str(today.year)
    two = datetime.datetime.strptime(birthday,"%d/%m/%Y")  # преобразование даты из строки в дату
    hour = (today - two).days*24+((today - two).seconds//3600)
    if (int(hour) < 0) or (int(day) <0) or (int(day) > 31) or (int(month) < 0) or (int(month) > 12):
        await message.answer("Вы ввели неверную дату")
        return
    # print(hour)
    but,but1 = await get_events(hours = hour)
    if len(but1) == 0:
        await message.answer("Нет доступных собеседований")
        return
    await state.update_data(events=but1)
    await message.answer("Выберете нужное собеседование", reply_markup=but)
    await SendRev.change_note_params.set()

async def change_note(message, state:FSMContext):
    data = await state.get_data()
    data = data['events']
    if message.text not in data:
        await message.answer("Используйте кнопки для выбора")
        return
    sobes = message.text
    await state.update_data(sobes=sobes)
    await message.answer("Какие именно данные вы хотите изменить ?", reply_markup= await change_parametrs_but())
    await SendRev.change_changing.set()

async def changing(message, state:FSMContext):
    if message.text == "ФИО":
        typ = "0"
        await message.answer("Введите новое имя")
        await SendRev.change_final.set()
    elif message.text == "Навыки":
        typ = "1"
        await message.answer("Введите новые навыки")
        await SendRev.change_final.set()
    elif message.text == "Образование":
        typ = "2"
        await message.answer("Введите новое образование")
        await SendRev.change_final.set()
    elif message.text == "Тип сотрудничества":
        typ = "3"
        await message.answer("Введите новый тип сотрудничества")
        await SendRev.change_final.set()
    elif message.text == "Опыт работы":
        typ = "4"
        await message.answer("Введите новый опыт работы")
        await SendRev.change_final.set()
    elif message.text == "Уровень в структуре":
        typ = "5"
        await message.answer("Введите новый уровень в структуре")
        await SendRev.change_final.set()
    elif message.text == "Уровень в hard Skils":
        typ = "6"
        await message.answer("Введите новый уровень в hard Skils")
        await SendRev.change_final.set()
    elif message.text == "Уровень в soft Skils":
        typ = "7"
        await message.answer("Введите новый уровень в soft Skils")
        await SendRev.change_final.set()
    elif message.text == "Общий коментарий":
        typ = "8"
        await message.answer("Введите новый общий коментарий")
        await SendRev.change_final.set()
    else:
        await message.answer("Используйте кнопки для выбора")
    await state.update_data(type=typ)

async def final_chnage(message,state:FSMContext):
    data = await state.get_data()
    sobes = data['sobes']
    typ = data['type']
    usr = message.from_user.username
    text = message.text
    await update_info(sobes,typ,text,usr)
    await message.answer("Изменения сохранены", reply_markup=hr_rev)
    await state.finish()
    await SendRev.login.set()
    

def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(start_fn,commands=["start"], state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")

def register_handlers_add_note(dp: Dispatcher):
    dp.register_message_handler(rev,state=SendRev.login)
    dp.register_message_handler(choose_date,state=SendRev.choose_date)
    dp.register_message_handler(chose_event,state=SendRev.choose_event)
    dp.register_message_handler(hard,state=SendRev.hard_rev)
    dp.register_message_handler(soft,state=SendRev.soft_rev)
    dp.register_message_handler(full,state=SendRev.full_rev)

def register_handlers_add_record(dp: Dispatcher):
    dp.register_message_handler(choose_video,state=SendRev.send_video)
    dp.register_message_handler(download_video,state=SendRev.pined_video,content_types=["photo","video","audio"])


def register_handlers_change_note(dp: Dispatcher):
    dp.register_message_handler(change_params,state=SendRev.change_note)
    dp.register_message_handler(change_note,state=SendRev.change_note_params)
    dp.register_message_handler(changing,state=SendRev.change_changing)
    dp.register_message_handler(final_chnage,state=SendRev.change_final)

register_handlers_main(dp)
register_handlers_add_note(dp)
register_handlers_add_record(dp)
register_handlers_change_note(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)