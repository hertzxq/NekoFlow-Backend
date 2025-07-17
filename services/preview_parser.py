import requests
from bs4 import BeautifulSoup
import json

API_URL = "http://127.0.0.1:8000/anime/all_anime"
PREVIEWS_FILE = "previews.json"


def fetch_anime_list():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        # исправлено:
        results = data.get("results", [])
        return [
            {"id": item.get("id"), "worldart_link": item.get("worldart_link")}
            for item in results
        ]
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return []


def parse_preview_images(anime_list):
    results = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for anime in anime_list:
        anime_id = anime.get("id")
        worldart_url = anime.get("worldart_link")

        if not worldart_url:
            continue

        try:
            response = requests.get(worldart_url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            a_tags = soup.find_all('a', href=lambda x: x and '/animation/animation_poster.php' in x)

            img_src = None
            for a_tag in a_tags:
                img_tag = a_tag.find('img')
                if img_tag and 'src' in img_tag.attrs:
                    img_src = img_tag['src']
                    if not img_src.startswith('http'):
                        img_src = f"http://www.world-art.ru{img_src}"
                    break

            if img_src:
                results.append({"id": anime_id, "image_src": img_src})

        except Exception as e:
            print(f"Ошибка при парсинге {worldart_url}: {e}")

    return results


def save_previews_to_file(previews):
    with open(PREVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(previews, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    anime_list = fetch_anime_list()
    previews = parse_preview_images(anime_list)
    save_previews_to_file(previews)
    print(f"Сохранено {len(previews)} превью в {PREVIEWS_FILE}")
