# syntax=docker/dockerfile:1

FROM python:3.7 AS builder

COPY requirements.txt /

RUN set -ex \
    && pip install --upgrade pip \
    && pip install --user --no-cache-dir -r requirements.txt

RUN curl https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o /usr/local/bin/wait-for-it \
    && chmod 655 /usr/local/bin/wait-for-it

FROM python:3.7-slim-buster AS runtime

RUN set -ex \
    && RUN_DEPS=" \
    libpq-dev \
    " \
    && apt-get update \
    && apt-get install -y --allow-unauthenticated --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*


COPY --from=builder /usr/local/bin/wait-for-it /usr/local/bin/
COPY --from=builder /root/.local/ /root/.local/

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

COPY src/ /app
COPY gunicorn-cfg.py  /app/
WORKDIR /app

CMD ["gunicorn", "--config", "gunicorn-cfg.py", "election_system.wsgi"]
