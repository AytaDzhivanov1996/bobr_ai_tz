import os
import requests
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

env_path = '.env'
load_dotenv(dotenv_path=env_path, override=True)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("API_KEY")
WEATHER_URL = "http://api.weatherapi.com/v1/current.json"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

def get_weather_data(city):
    params = {
        "q": city,
        "key": API_KEY,
        "aqi": False,
        "lang": "ru"
    }
    response = requests.get(WEATHER_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply("Привет! Отправь мне название города, и я покажу тебе погоду в нем")

@dp.message()
async def get_weather(message: types.Message):
    city = message.text.strip()
    weather_data = get_weather_data(city)

    if weather_data:
        temp = weather_data["current"]["temp_c"]
        descr = weather_data["current"]["condition"]["text"]
        humidity = weather_data["current"]["humidity"]
        response = (
            f"Погода в городе {city}:\n\n"
            f"Описание: {descr}\n"
            f"Температура: {temp}°C\n"
            f"Влажность: {humidity}%"
        )
    else:
        response = f"Не удалось найти погоду для города {city}. Проверьте правильность написания."
    
    await message.answer(response)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
