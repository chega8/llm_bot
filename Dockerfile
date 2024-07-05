FROM python:3.11

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install --no-root

COPY ./data /app/data
COPY ./src /app/src
COPY .env /app/.env

CMD ["poetry", "run", "python", "src/app.py"]
