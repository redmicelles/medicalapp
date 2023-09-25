FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get --yes install apt-utils

RUN pip install poetry==1.6.1

WORKDIR /medicalapp

COPY poetry.lock pyproject.toml /medicalapp/

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction

COPY . /medicalapp/