import datetime

import requests
import re
import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class Interlayer(StatesGroup):
    just = State()
    just2 = State()


class PersonInfo(StatesGroup):
    gender = State()
    year_birth = State()
    months_birth = State()
    day_birth = State()
    time_birth = State()
    city_birth = State()

storage = MemoryStorage()

token = 
password =

bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)


headers = {

}


def gen_markup(quanity: int, row_width: int) -> InlineKeyboardMarkup:
    # код для добавления кнопок с выбором дня рождения
    markup = InlineKeyboardMarkup(row_width=row_width)
    for i in range(1, quanity):
        markup.insert(InlineKeyboardButton(f"{i}", callback_data=f"{i}"))
    return markup


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    inline_btn_1 = InlineKeyboardButton('Старт!', callback_data='button1')
    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
    photo = InputFile("")
    await bot.send_photo(message.from_user.id, photo=photo,
                         caption="...",
                         reply_markup=inline_kb1)

@dp.callback_query_handler(lambda c: c.data == 'button1')
async def Gender(callback_query: types.CallbackQuery, state: FSMContext):
    # код для обработки пола

    women = InlineKeyboardButton('...', callback_data='f')
    man = InlineKeyboardButton('...', callback_data='m')
    choice = InlineKeyboardMarkup().add(women, man)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '...', reply_markup=choice)
    url = "..."
    _password = {"password": "..."}
    requests.post(url, data=_password)
    await PersonInfo.gender.set()


@dp.callback_query_handler(state=PersonInfo.gender)
async def Year(callback_query: types.CallbackQuery, state: FSMContext):
    # код для обработки года
    gender = callback_query.data
    if gender == 'm' or gender == 'f':
        await state.update_data(gender=gender)
        await bot.send_message(callback_query.from_user.id, '...')
        await PersonInfo.year_birth.set()
    else:
        await bot.send_video(callback_query.from_user.id, '...')
        await bot.send_message(callback_query.from_user.id,
                               '...')
        await Gender(callback_query, state)

@dp.message_handler(state=PersonInfo.year_birth)
async def Month(msg: types.Message, state: FSMContext):
    # код для обработки месяца
    year = datetime.date.today().year
    regular_expression = r'^(19[5-9]\d|20\d{2})$'
    if re.match(regular_expression, msg.text):
        if int(msg.text) < (year - 70) or int(msg.text) > year:
            await bot.send_message(msg.from_user.id,
                                   '...')
            return Month
        else:
            await state.update_data(year=msg.text)
            January = InlineKeyboardButton('...', callback_data='01')
            February = InlineKeyboardButton('🌸 ...', callback_data='02')
            March = InlineKeyboardButton('🌹 ...', callback_data='03')
            April = InlineKeyboardButton('🪷 ...', callback_data='04')
            May = InlineKeyboardButton('🌻 ...', callback_data='05')
            June = InlineKeyboardButton('🌈 ...', callback_data='06')
            July = InlineKeyboardButton('🌞 ...', callback_data='07')
            August = InlineKeyboardButton('🍀 ...', callback_data='08')
            September = InlineKeyboardButton('🍁 ...', callback_data='09')
            October = InlineKeyboardButton('🍂 ...', callback_data='10')
            November = InlineKeyboardButton('☃️ ...', callback_data='11')
            December = InlineKeyboardButton('🎄 ...', callback_data='12')
            months = InlineKeyboardMarkup().add(January, February, March, April, May, June, July, August, September, October, November, December)

            await bot.send_message(msg.from_user.id, '.', reply_markup=months)
            await PersonInfo.months_birth.set()
    else:
        await bot.send_message(msg.from_user.id,
                               '...')
        return Month

@dp.callback_query_handler(state=PersonInfo.months_birth)
async def Day(callback_query: types.CallbackQuery, state: FSMContext):
    month = callback_query.data
    await state.update_data(month=month)
    # код для обработки дня

    choice = gen_markup(31, 7)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '...', reply_markup=choice)
    await PersonInfo.day_birth.set()


@dp.callback_query_handler(state=PersonInfo.day_birth)
async def ConfirmDate(callback_query: types.CallbackQuery, state: FSMContext):
    day = callback_query.data
    await state.update_data(day=day)
    data = await state.get_data()
    # код для вывода даты, и опроса, верная ли она
    check_day = r'^([0-9]|1[0-9]|2[0-9]|30)?$'
    check_month = r'^(0[0-9]|1[0-2])?$'
    check_year = r'^(19[5-9]\d|20\d{2})$'
    if not re.match(check_day, data['day']) or not re.match(check_month, data['month']) or not re.match(check_year, data['year']):
        await bot.send_video(callback_query.from_user.id, '...')
        await bot.send_message(callback_query.from_user.id,
                               '...')
        await Year(callback_query, state)
    else:
        yes = InlineKeyboardButton('...', callback_data='yes')
        no = InlineKeyboardButton('...', callback_data='no')
        choice = InlineKeyboardMarkup().add(yes, no)
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, f"...: {data['day']}.{data['month']}.{data['year']} года", reply_markup=choice)
        await Interlayer.just2.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'yes', state=Interlayer.just2)
async def handle_yes(callback_query: types.CallbackQuery, state: FSMContext):
    # код для обработки выбора "Да"
    await bot.send_message(callback_query.from_user.id, '...')
    await PersonInfo.time_birth.set()



@dp.callback_query_handler(lambda callback_query: callback_query.data == 'no', state=Interlayer.just2)
async def handle_no(callback_query: types.CallbackQuery, state: FSMContext):
    # код для обработки выбора "Нет"
    await Year(callback_query, state)


@dp.message_handler(state=PersonInfo.time_birth)
async def City(msg: types.Message, state: FSMContext):
    # код для обработки города
    regular_expression = r'^([01]\d|2[0-3]):([0-5]\d)$'
    if not re.match(regular_expression, msg.text):
        await bot.send_message(msg.from_user.id,
                               '...')
        return ConfirmDate
    else:
        await state.update_data(time=msg.text)

        await bot.send_message(msg.from_user.id,
                               '...')
        await PersonInfo.city_birth.set()



@dp.message_handler(state=PersonInfo.city_birth)
async def AllInfo(msg: types.Message, state: FSMContext):
    await state.update_data(city=msg.text)
    data = await state.get_data()
    gender = "..." if data['gender'] == "..." else "..."

    yes = InlineKeyboardButton('...', callback_data='YES')
    no = InlineKeyboardButton('...', callback_data='NO')
    choice = InlineKeyboardMarkup().add(yes, no)
    await bot.send_message(msg.from_user.id,
                           f"...:\n\n"
                           f"...: {gender}\n"
                           f"...: {data['day']}.{data['month']}.{data['year']}\n"
                           f"...: {data['city']}\n"
                           f"...: {data['time']}\n",
                           reply_markup=choice)
    await Interlayer.just.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'NO', state=Interlayer.just)
async def Handler_NO(callback_query: types.CallbackQuery, state: FSMContext):
    await Gender(callback_query, state)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'YES', state=Interlayer.just)
async def FinishAndPost(callback_query: types.CallbackQuery, state: FSMContext):
    #post запрос
    just = callback_query.data
    await state.update_data(password=password, just=just)
    data = await state.get_data()
    url = "..."
    response = requests.post(url, data=data)
    data_server = json.loads(response.text)

    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton('...', url=data_server["data"])
    keyboard.add(button)

    if data_server['status'] == "ok":
        if data_server['data'] is not None:
            photo = InputFile('...')
            await bot.send_photo(callback_query.from_user.id, photo=photo,
                                caption=f'...', parse_mode="HTML", reply_markup=keyboard)
    else:
        await bot.send_video(callback_query.from_user.id, '...')
        await bot.send_message(callback_query.from_user.id,
                               '...')
    await state.finish()

executor.start_polling(dp)
