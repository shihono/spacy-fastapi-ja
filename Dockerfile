FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
ENV PORT 8080
ENV APP_MODULE app.api:app
ENV LOG_LEVEL debug
ENV WEB_CONCURRENCY 2

RUN mkdir -p /usr/src/ && mkdir /log
WORKDIR /usr/src/

COPY . /usr/src/
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev
