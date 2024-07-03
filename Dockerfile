FROM python:3.9-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt && apk update && apk add curl

ENV PORT=5000

EXPOSE $PORT

VOLUME ["/app/data"]

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT HBnB_App:app"]