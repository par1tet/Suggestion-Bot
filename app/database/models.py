from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=True)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

#Users table
class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    tg_id = mapped_column(BigInteger()) #Telegram id user
    user_full_name: Mapped[str] = mapped_column(String(60))#Full name user
    is_admin: Mapped[bool] = mapped_column()#Admin or not
    
class Suggest(Base):
    __tablename__ = 'suggests'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    who_suggest_full_name: Mapped[str] = mapped_column(String(60))#Who suggest full name
    who_suggest_id = mapped_column(BigInteger())#Who suggest id
    is_answer: Mapped[bool] = mapped_column()#Answer or not
    
    suggest: Mapped[str] = mapped_column(String(1000))#The suggest
    media_id: Mapped[str] = mapped_column(String(100))#Media id(photo)
    
#Create db
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)