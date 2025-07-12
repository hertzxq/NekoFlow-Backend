import aiohttp
import certifi
import ssl
from core.config import KODIK_API_KEY

async def fetch_all_anime():
    async with aiohttp.ClientSession() as session:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with session.get(
                f'https://kodikapi.com/list?token={KODIK_API_KEY}&types=anime-serial',
                ssl=ssl_context) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return {"error": f"Request failed with status {response.status}"}

async def fetch_anime(title: str):
    async with aiohttp.ClientSession() as session:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with session.get(
                f'https://kodikapi.com/search?token={KODIK_API_KEY}&title={title}&limit=1',
                ssl=ssl_context) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return {"error": f"Request failed with status {response.status}"}

async def fetch_anime_by_id(anime_id: str):
    async with aiohttp.ClientSession() as session:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with session.get(
                f'https://kodikapi.com/search?token={KODIK_API_KEY}&id={anime_id}',
                ssl=ssl_context) as response:
            if response.status == 200:
                data = await response.json()
                if data.get('results') and len(data['results']) > 0:
                    result = data['results'][0]
                    return {
                        "title": result.get("title", "Unknown Title"),
                        "year": result.get("year", None),
                        "shikimori_id": result.get("shikimori_id", None),
                        "kodik_id": result.get("id", None),
                        "type": result.get("type", "serial"),
                        "link": result.get("link", None),  # Добавляем link
                        "translation": result.get("translation", None)  # Добавляем translation
                    }
                return None
            else:
                return {"error": f"Request failed with status {response.status}"}