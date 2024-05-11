from app.database.models import User,Suggest,async_session
import asyncio
from sqlalchemy import select, update, delete

async def new_user(tg_id: int, full_name: str) -> None:
    async with async_session() as session:
        # Checking if there is a user in the database
        # Returns False if the user exists in the database
        if (True if len([i for i in [i.tg_id for i in await session.scalars(select(User))] if i == tg_id]) == 0 else False):
            session.add(User(tg_id=tg_id, user_full_name=full_name, is_admin=False))
            await session.commit()
            
async def add_suggest(suggest: str, tg_us: int,  full_name: str) -> None:
    async with async_session() as session:
        # Add new suggest
        session.add(Suggest(who_suggest_full_name=full_name, who_suggest_us=tg_us, answer_text='', suggest_text=suggest,media_id='idk'))
        await session.commit()
        
async def get_suggests():
    async with async_session() as session:
        # Get sugget
        suggests = await session.scalars(select(Suggest))
        return [i for i in suggests]