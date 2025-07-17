from fastapi import APIRouter, HTTPException
from services.http_kodik import fetch_all_anime, fetch_anime, fetch_anime_by_id
import logging
import json

logger = logging.getLogger(__name__)

anime_router = APIRouter(prefix="/anime", tags=["Anime"])

PREVIEWS_FILE = "./services/previews.json"


def load_previews():
    """
    Загружает превьюшки из локального файла и возвращает словарь id -> image_src.
    """
    try:
        with open(PREVIEWS_FILE, "r", encoding="utf-8") as f:
            previews = json.load(f)
            return {str(item["id"]).strip(): item["image_src"] for item in previews}
    except Exception as e:
        logger.error(f"Не удалось загрузить превью: {e}")
        return {}


@anime_router.get("/all_anime")
async def all_anime():
    try:
        data = await fetch_all_anime()
        logger.debug(f"Raw response from fetch_all_anime: {data}")

        if not data or "results" not in data:
            logger.error(f"Invalid response format: {data}")
            return {"error": "Invalid response format from fetch_all_anime"}

        anime_results = data["results"]

        id_to_image = load_previews()

        for item in anime_results:
            item_id = str(item.get("id")).strip()
            image_src = id_to_image.get(item_id)
            logger.debug(f"Trying: {item_id} -> {image_src}")
            if image_src:
                item["image_src"] = image_src

        logger.info("Fetched all anime with images")
        data["results"] = anime_results
        return data

    except Exception as e:
        logger.error(f"Error fetching all anime: {str(e)}")
        return {"error": str(e)}


@anime_router.get("/search_anime")
async def search_anime(anime_title: str):
    try:
        # Запрашиваем список
        data = await fetch_anime(title=anime_title)
        logger.debug(f"Raw response from fetch_anime: {data}")

        id_to_image = load_previews()

        # Если результат dict с ключом results
        if isinstance(data, dict) and "results" in data:
            for item in data["results"]:
                # Нормализуем ключ
                item_id = None
                if item.get("id"):
                    item_id = str(item.get("id")).strip()
                elif item.get("kodik_id"):
                    item_id = str(item.get("kodik_id")).strip()

                logger.debug(f"Trying search_anime match_id: {item_id}")

                image_src = id_to_image.get(item_id)
                logger.debug(f"Search image_src for {item_id}: {image_src}")

                if image_src:
                    item["image_src"] = image_src

        # Если вдруг результат это список (редко, но вдруг)
        elif isinstance(data, list):
            for item in data:
                item_id = None
                if item.get("id"):
                    item_id = str(item.get("id")).strip()
                elif item.get("kodik_id"):
                    item_id = str(item.get("kodik_id")).strip()

                logger.debug(f"Trying search_anime match_id: {item_id}")

                image_src = id_to_image.get(item_id)
                logger.debug(f"Search image_src for {item_id}: {image_src}")

                if image_src:
                    item["image_src"] = image_src

        logger.info(f"Searched anime with title: {anime_title}")
        return {"success": data}

    except Exception as e:
        logger.error(f"Error searching anime: {str(e)}")
        return {"error": str(e)}



@anime_router.get("/current_anime")
async def get_anime_by_id(anime_id: str):
    try:
        data = await fetch_anime_by_id(anime_id)
        if not data:
            logger.warning(f"Anime with ID {anime_id} not found")
            raise HTTPException(status_code=404, detail="Anime not found")

        id_to_image = load_previews()

        # Явно нормализуем match_id:
        match_id = None
        if data.get("id"):
            match_id = str(data.get("id")).strip()
        elif data.get("kodik_id"):
            match_id = str(data.get("kodik_id")).strip()

        logger.debug(f"Trying current_anime match_id: {match_id}")
        image_src = id_to_image.get(match_id)

        logger.debug(f"Image src for match_id {match_id}: {image_src}")

        response = {
            "title": data.get("title", "Unknown Title"),
            "year": data.get("year", None),
            "shikimori_id": data.get("shikimori_id", None),
            "kodik_id": data.get("kodik_id", None),
            "type": data.get("type", "serial"),
            "link": data.get("link", None),
            "translation": data.get("translation", None),
            "image_src": image_src
        }

        logger.info(f"Fetched anime with ID {anime_id}: {response}")
        return {"success": response}

    except Exception as e:
        logger.error(f"Error fetching anime ID {anime_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching anime: {str(e)}")
