from fastapi import APIRouter, HTTPException
from services.http_kodik import fetch_all_anime, fetch_anime, fetch_anime_by_id
import logging

logger = logging.getLogger(__name__)

anime_router = APIRouter(prefix="/anime", tags=["Anime"])

@anime_router.get("/all_anime")
async def all_anime():
    try:
        data = await fetch_all_anime()
        logger.info("Fetched all anime")
        return {"success": data}
    except Exception as e:
        logger.error(f"Error fetching all anime: {str(e)}")
        return {"error": str(e)}

@anime_router.get("/search_anime")
async def search_anime(anime_title: str):
    try:
        data = await fetch_anime(title=anime_title)
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
        response = {
            "title": data.get("title", "Unknown Title"),
            "year": data.get("year", None),
            "shikimori_id": data.get("shikimori_id", None),
            "kodik_id": data.get("kodik_id", None),
            "type": data.get("type", "serial"),
            "link": data.get("link", None),
            "translation": data.get("translation", None)
        }
        logger.info(f"Fetched anime with ID {anime_id}: {response}")
        return {"success": response}
    except Exception as e:
        logger.error(f"Error fetching anime ID {anime_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching anime: {str(e)}")