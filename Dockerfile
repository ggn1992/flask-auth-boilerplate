FROM python:3.12.4-alpine3.20

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP wsgi.py

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]
