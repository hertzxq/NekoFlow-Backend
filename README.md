<div align="center">

<h1>NekoFlow — Backend (FastAPI)</h1>

<p>
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.1x-009485?logo=fastapi&logoColor=white" />
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white" />
  <img alt="SQLAlchemy" src="https://img.shields.io/badge/SQLAlchemy-async-9b59b6" />
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-asyncpg-336791?logo=postgresql&logoColor=white" />
  <img alt="Auth" src="https://img.shields.io/badge/Auth-JWT-000" />
</p>

<p>Сервис API для проекта NekoFlow. Отвечает за аутентификацию, доступ к данным пользователей и интеграцию с внешним API Kodik для каталога аниме. Предназначен для использования с фронтендом <code>NekoFlow-Frontend</code>.</p>

</div>

### ✨ Возможности
- Регистрация пользователя (`/users`) с хэшированием пароля (bcrypt)
- Логин и выдача JWT (`/login`) на базе `authx`
- Защищённый пример эндпоинта (`/protected`)
- Каталог/поиск/получение тайтла через Kodik API (`/anime/*`)
- CORS для фронтенда (по умолчанию `http://localhost:3000`)

### 🧰 Стек
- FastAPI, Uvicorn
- SQLAlchemy (async), PostgreSQL (`asyncpg`)
- Pydantic, AuthX (JWT), passlib[bcrypt]
- Aiohttp, certifi (Kodik API)
- Python‑dotenv

### 🚀 Быстрый старт
1. Установите зависимости:
```bash
pip install -r requirements.txt
```
Если файла `requirements.txt` нет, пример минимального набора:
```bash
pip install fastapi uvicorn[standard] sqlalchemy[asyncio] asyncpg pydantic authx passlib[bcrypt] python-dotenv aiohttp certifi
```

2. Настройте переменные окружения в `.env` (рядом с `main.py`):
```env
KODIK_API_KEY=ваш_kodik_token
SECRET_KEY=случайная_строка_для_jwt

DB_NAME=nekoflow
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

3. Поднимите PostgreSQL (локально или в Docker) и убедитесь, что доступ по `DATABASE_URL` корректен.

4. Запустите сервер:
```bash
python main.py
```
API будет доступен на `http://127.0.0.1:8000` (Swagger: `/docs`).

### 🧪 Основные эндпоинты
- `GET /` — статус
- `POST /users` — создать пользователя
- `POST /login` — получить JWT токен
- `GET /protected` — пример защищённого ресурса (нужен токен)
- `GET /anime/all_anime` — список аниме (через Kodik API) с подстановкой превью из `previews.json`
- `GET /anime/search_anime?anime_title=...` — поиск
- `GET /anime/current_anime?anime_id=...` — данные по тайтлу

### 🗂️ Структура проекта
- `main.py` — приложение FastAPI, CORS, маршруты, auth, БД‑сессии
- `core/config.py` — конфиг/переменные окружения (`KODIK_API_KEY`, `SECRET_KEY`, `DATABASE_URL`)
- `database/models.py` — движок БД, модель `UsersModel`, `init_db`
- `database/shema.py` — Pydantic‑схемы (`UsersShema`, `LoginShema`)
- `services/anime_router.py` — роутер `/anime`, склейка превью с данными Kodik
- `services/http_kodik.py` — запросы к Kodik API (aiohttp)
- `services/preview_parser.py` — утилита для парсинга превью и записи в `previews.json`

<details>
<summary><b>Заметки по превью</b></summary>

- `services/previews.json` содержит соответствия `id -> image_src`.
- `preview_parser.py` можно использовать для заполнения файла, при условии доступности `API_URL`.

</details>

### 📝 Примечания
- Убедитесь, что CORS разрешает адрес фронтенда; измените список `origins` в `main.py` при необходимости.
- Токены Kodik имеют ограничения и политику использования — храните `KODIK_API_KEY` в `.env`.
- Пароли хранятся в виде bcrypt‑хэшей; никогда не храните их в открытом виде.

### 👤 Автор
- Автор: `@hertzxq`
- Email: `nounfeed@gmail.com`

