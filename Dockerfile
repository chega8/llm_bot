FROM python:3.9

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . /app

CMD ["poetry", "run", "python", "src/app.py"]
