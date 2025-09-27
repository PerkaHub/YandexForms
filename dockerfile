FROM python:3.12-slim

RUN pip install uv

WORKDIR /src

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen 

COPY . .

CMD [".venv/bin/gunicorn", "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]