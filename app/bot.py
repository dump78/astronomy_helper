from aiogram import Bot, types, Dispatcher
from app.keyboards import inline_kb, keyboard
from app.dialogs import MESSAGES, input_field_text, text_get_coords, text_planet_data, planets_eng_rus
from config import TOKEN, API_URL
import logging
import requests
import json


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
location = None


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(MESSAGES['start'].format(message.from_user.first_name), reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer(MESSAGES['help'])


@dp.message_handler(lambda message: message.text == text_get_coords)
async def process_coords_command(message: types.Message):
    await message.answer(MESSAGES['coords'], reply_markup=keyboard)


@dp.message_handler(content_types=["location"])
async def process_get_location(message: types.Message):
    global location
    location = message.location
    await message.answer(input_field_text, reply_markup=inline_kb)


@dp.callback_query_handler(lambda c: c.data)
async def send_planet_coords(callback_query: types.CallbackQuery):
    planet_tuple = planets_eng_rus[callback_query.data]
    planet_name_rus = planet_tuple[0]
    planet_num = planet_tuple[1]
    if location is not None:
        latitude = location.latitude
        longitude = location.longitude
        api_url = API_URL.format(latitude, longitude)
    else:
        await callback_query.message.answer(MESSAGES['error_geo_message'])
    r = requests.get(url=api_url)
    if r.status_code == 200:
        data = json.loads(r.text)
        planet_data = data['data'][planet_num]
        right_ascension = planet_data['rightAscension']['raw']
        declination = planet_data['declination']['raw']
        if data is not None:
            await callback_query.message.answer(text=text_planet_data.format(planet_name_rus, right_ascension, declination), reply_markup=inline_kb)
        else:
            await callback_query.message.answer(MESSAGES['error_find_data_message'])
    else:
        await callback_query.message.answer(MESSAGES['error_load_data_message'])


@dp.message_handler()
async def another_message(message: types.Message):
    await message.answer(MESSAGES['another_text'])
