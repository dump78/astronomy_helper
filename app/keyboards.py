from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.dialogs import placeholder, text_get_coords, text_send_location


inline_btn_sun = InlineKeyboardButton('Солнце', callback_data='Sun')
inline_btn_moon = InlineKeyboardButton('Луна', callback_data='Moon')
inline_btn_mercury = InlineKeyboardButton('Меркурий', callback_data='Mercury')
inline_btn_venus = InlineKeyboardButton('Венера', callback_data='Venus')
inline_btn_mars = InlineKeyboardButton('Марс', callback_data='Mars')
inline_btn_jupiter = InlineKeyboardButton('Юпитер', callback_data='Jupiter')
inline_btn_saturn = InlineKeyboardButton('Сатурн', callback_data='Saturn')
inline_btn_uranus = InlineKeyboardButton('Уран', callback_data='Uranus')
inline_btn_neptune = InlineKeyboardButton('Нептун', callback_data='Neptune')

inline_kb = InlineKeyboardMarkup().add(inline_btn_sun, inline_btn_moon, inline_btn_mercury, inline_btn_venus,
                                       inline_btn_mars, inline_btn_jupiter, inline_btn_saturn, inline_btn_uranus,
                                       inline_btn_neptune)

kb = [
        [
            types.KeyboardButton(text=text_get_coords)
        ],
        [
            types.KeyboardButton(text=text_send_location, request_location=True)
        ]
    ]

keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    input_field_placeholder=placeholder
)
