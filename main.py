import asyncio
import aiohttp
import requests
from database import database_main

URL = 'https://swapi.dev/api/people/'

async def get_character(url: str):
    async with aiohttp.client.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

def title_generator(url_list):
    try:
        for url in url_list:
            result = requests.get(url)
            yield result.json()['name']
    except KeyError:
        for url in url_list:
            result = requests.get(url)
            yield result.json()['title']

async def get_homeworld_name(url: str):
    async with aiohttp.client.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def get_sw_character():
    sw_character_list = list()
    characters_tasks = [get_character(f'{URL}/{i}') for i in range(1, 10)]
    characters_info = await asyncio.gather(*characters_tasks)
    for person in characters_info:
        data = dict()
        data['birth_year'] = person['birth_year']
        data['eye_color'] = person['eye_color']
        data['films'] = ', '.join(title_generator(person['films']))
        data['gender'] = person['gender']
        data['hair_color'] = person['hair_color']
        data['height'] = person['height']
        planet = await get_homeworld_name(person['homeworld'])
        data['homeworld'] = planet['name']
        data['mass'] = person['mass']
        data['name'] = person['name']
        data['skin_color'] = person['skin_color']
        data['species'] = ', '.join(title_generator(person['species']))
        data['starships'] = ', '.join(title_generator(person['starships']))
        data['vehicles'] = ', '.join(title_generator(person['vehicles']))

        sw_character_list.append(data)
    return list(sw_character_list)

async def main():
    sw_characters = await get_sw_character()
    await database_main(sw_characters)

asyncio.run(main())



