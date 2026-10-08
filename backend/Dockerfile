FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./backend/app
COPY backend/api ./backend/api
COPY backend/config ./backend/config
COPY backend/services ./backend/services
COPY backend/utils ./backend/utils
COPY models ./models

ENV PYTHONPATH=/app/backend

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]