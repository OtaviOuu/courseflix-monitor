#!/usr/bin/env python3
import asyncio
import aiohttp
from dotenv import load_dotenv
import os

from scraper import Scraper
from db import db

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


async def send_message(message):
    asyncio.sleep(1)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params) as response:
            if response.status == 200:
                print(f"Message sent: {message}")
            else:
                print(f"Failed to send message: {response.status}")


async def main():
    scraper = Scraper()

    html = await scraper._get_courses_in_page(1)
    courses = await scraper._parse_courses(html)

    for course in courses:
        if db.get(course):
            continue
        db.set(course, course)
        await send_message(course)


if __name__ == "__main__":
    asyncio.run(main())
