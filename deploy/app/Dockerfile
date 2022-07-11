FROM python:3.9-slim

RUN apt-get update && apt-get install -y git

WORKDIR /opt/app

COPY ./app/pyproject.toml ./app/poetry.lock ./

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install

COPY ./app .

EXPOSE 5000

CMD ["poetry", "run", "python", "-m", "web.app"]