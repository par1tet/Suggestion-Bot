from aiogram import Bot, Dispatcher
from os import getenv as gt
from dotenv import load_dotenv as ld
import logging
import asyncio

# Import db
from app.database.models import async_main

# Import router
from app.handlers import r

ld()

async def main():
    # Create db
    await async_main()
    
    # Create bot and dispatcher
    bot = Bot(token=gt("TOKEN_BOT"))
    dp =  Dispatcher()
    
    # Start polling
    dp.include_router(r)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    # Logging
    logging.basicConfig(level=logging.INFO)
    # Start main function
    asyncio.run(main())