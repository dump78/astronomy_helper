from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.keyboards import inline_kb, keyboard
from app.dialogs import MESSAGES, input_field_text, text_get_coords, text_planet_data, planets_eng_rus
from config import TOKEN, API_URL
import aiohttp
import logging


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.DEBUG)


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
async def process_get_location(message: types.Message, state: FSMContext):
    try:
        await state.finish()
        location = message.location
        async with state.proxy() as data:
            data['location'] = location
        await message.answer(input_field_text, reply_markup=inline_kb)
    except Exception:
        await message.answer(MESSAGES['error_geo_message'])
        raise


@dp.callback_query_handler(lambda c: c.data)
async def send_planet_coords(callback_query: types.CallbackQuery, state: FSMContext):
    planet_tuple = planets_eng_rus[callback_query.data]
    planet_name_rus = planet_tuple[0]
    planet_num = planet_tuple[1]
    async with state.proxy() as data:
        try:
            location = data['location']
            latitude = location.latitude
            longitude = location.longitude
            api_url = API_URL.format(latitude, longitude)
        except Exception:
            await callback_query.message.answer(MESSAGES['error_geo_message'])
            raise
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            data = await response.json()
            if response.status == 200:
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
