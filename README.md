# spacy-fastapi-ja

Spacy ([Japanese model](https://spacy.io/models/ja)) + FastAPI

This is based on [cookiecutter-spacy-fastapi](https://github.com/microsoft/cookiecutter-spacy-fastapi)

## Quick Start

This project requires [Poetry](https://python-poetry.org/).

```python
# install
poetry install

# run locally
poetry run uvicorn app.api:app --reload
# or 
poetry run python main.py

# test
poetry run pytest
```

### gunicorn

```bash
poetry run gunicorn main:app --config ./gunicorn.conf.py 
```

### Docker

Run with Docker image [uvicorn-gunicorn-docker](https://github.com/tiangolo/uvicorn-gunicorn-docker)

```bash
docker-compose build
docker-compose up -d
```