from app.database.models import User,Suggest,async_session
import asyncio
from sqlalchemy import select, update, delete

async def new_user(tg_id, full_name):
    async with async_session() as session:
        #Checking if there is a user in the database
        #Returns False if the user exists in the database
        if (True if len([i for i in [i.tg_id for i in await session.scalars(select(User))] if i == tg_id]) == 0 else False):
            session.add(User(tg_id=tg_id, user_full_name=full_name, is_admin=False))
            await session.commit()
            
async def add_suggest(suggest, tg_id,  full_name):
    async with async_session() as session:
        session.add(Suggest())