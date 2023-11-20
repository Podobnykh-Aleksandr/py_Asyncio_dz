import asyncio
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config

Base = declarative_base()

class SWСharacter(Base):

    __tablename__ = 'star_war_character'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_year = Column(String)
    eye_color = Column(String)
    films = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    skin_color = Column(String)
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)

async def database_main(data):

    engine = create_async_engine(config.PG_DSN_ALC, echo=True)

    async with engine.begin() as start:
        await start.run_sync(Base.metadata.drop_all)
        await start.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:
        async with session.begin():
            for person in data:
                сharacter = SWСharacter(
                    name=person['name'],
                    birth_year=person['birth_year'],
                    eye_color=person['eye_color'],
                    films=person['films'],
                    gender=person['gender'],
                    hair_color=person['hair_color'],
                    height=person['height'],
                    homeworld=person['homeworld'],
                    mass=person['mass'],
                    skin_color=person['skin_color'],
                    species=person['species'],
                    starships=person['starships'],
                    vehicles=person['vehicles'],
                )
                session.add(сharacter)

        await session.commit()
