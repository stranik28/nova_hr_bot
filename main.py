from importlib.metadata import metadata
from buttons import hr_rev,get_events
from config import api
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from bd import insert_val_min,add_video

bot = Bot(token=api)

dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

class SendRev(StatesGroup):
    login = State()
    choose_event = State()
    hard_rev = State()
    soft_rev = State()
    full_rev = State()

    send_video = State()
    pined_video = State()

usernames = ["reaL_IdpNik","Artemsm67","cris_tee","foxyess2020"]

async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())

async def start_fn(message: types.Message):
    if message.from_user.username in usernames:
        await SendRev.login.set()
        await message.answer("Hello "+ message.from_user.full_name, reply_markup=hr_rev)
    else:
        await message.reply("You are not allowed to use this bot")

async def rev(message: types.Message, state: FSMContext):
    print(message.text)
    if message.text == "Добавить информацию о собеседовании":
        but,but1 = await get_events()
        await message.answer("Выберете нужное собеседование", reply_markup=but)
        await SendRev.next()
        await state.update_data(events=but1)
    elif message.text == "Добавить запись собеседования":
        but,but1 = await get_events()
        await message.answer("Выберете нужное собеседование", reply_markup=but)
        await SendRev.send_video.set()
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

def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(start_fn,commands=["start"], state="*")
    dp.register_message_handler(rev,state=SendRev.login)
    dp.register_message_handler(chose_event,state=SendRev.choose_event)
    dp.register_message_handler(hard,state=SendRev.hard_rev)
    dp.register_message_handler(soft,state=SendRev.soft_rev)
    dp.register_message_handler(full,state=SendRev.full_rev)

    dp.register_message_handler(choose_video,state=SendRev.send_video)
    # tt = types.ContentType.VIDEO
    # tt = types.ContentType.PHOTO
    # tt = types.ContentType.AUDIO
    dp.register_message_handler(download_video,state=SendRev.pined_video,content_types=["photo","video","audio"])

register_handlers_main(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)