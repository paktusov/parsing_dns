FROM python:3.9-slim

RUN apt-get update && apt-get install -y git

RUN pip install poetry

WORKDIR /opt/app

COPY pyproject.toml poetry.lock .

RUN poetry install

COPY . .

EXPOSE 5000

CMD ["python", "-m", "web.py"]