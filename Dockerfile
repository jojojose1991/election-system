FROM python:3.7

COPY requirements.txt /
RUN set -ex \
    && pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

COPY src/ /app
WORKDIR /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
