FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_VERSION=1.0.0
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

WORKDIR /manage_books

RUN pip install "poetry==$POETRY_VERSION"

COPY ./pyproject.toml ./poetry.lock* /manage_books/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

COPY . ./manage_books/

