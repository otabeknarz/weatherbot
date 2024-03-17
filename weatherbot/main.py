import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from parsing import get_weather
from download import download_file

API_TOKEN = '7100832003:AAGrm9Glxxo3_3b9hMMtKZvwDq-xS4GrLXU'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

keyboard = InlineKeyboardMarkup()
cities = {'Toshkent': 'tashkent', 'Andijon': 'andijan', 'Buxoro': 'bukhara', 'Guliston': 'gulistan', 'Jizzax': 'jizzakh',
          'Zarafshon': 'zarafshan', 'Qarshi': 'karshi', 'Navoiy': 'navoi', 'Namangan': 'namangan', 'Nukus': 'nukus',
          'Samarqand': 'samarkand', 'Termiz': 'termez', 'Urganch': 'urgench', "Farg'ona": 'ferghana', 'Xiva': 'khiva'}

buttons = []
for city, url in cities.items():
    if len(buttons) == 2:
        keyboard.row(*buttons)
        buttons.clear()
    buttons.append(InlineKeyboardButton(city, callback_data=url))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Manzilingizni yuboring", reply_markup=keyboard)


@dp.callback_query_handler()
async def send_weather(call: types.CallbackQuery):
    message = call.data
    weather = get_weather(message)
    icon_path = download_file(weather['today'][-1], weather['today'][-1].split('/')[-1].split('.')[0])
    if icon_path:
        icon = open(icon_path, 'rb')
    caption = f"{message} dagi ob-havo\n{weather['today'][0]}\nEng baland harorat: {weather['today'][1][0]}\nEng past harorat: {weather['today'][1][1]}"
    for day, temps in weather['week'].items():
        caption += f"\n{day}: {temps[0].text} va {temps[1].text}"

    await call.bot.send_photo(call.from_user.id, icon, caption=caption)

    icon.close()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
