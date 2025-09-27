# YandexForms

**Стек:** Python 3.12, FastAPI, PostgreSQL, SQLAlchemy

1. Клонируйте репозиторий:
```sh
git clone git@github.com:PerkaHub/YandexForms.git
cd YandexForms/
```
    
2. Перейдиье в директорию infra/ и создайте `.env` файл:
```sh
cd infra/
```

```
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=postgres
DB_DRIVER=postgresql+asyncpg

SECRET_KEY=AbObUs
ALGORITHM=HS256
```

3. Запустите проект через Docker Compose:
```sh
docker compose build
docker compose up
```

  
