FROM python:3.9.7-slim-buster
RUN mkdir /app
WORKDIR /app

RUN apt update
RUN apt install -y libpq-dev curl gcc gdal-bin
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
COPY ./poetry.toml /app/poetry.toml
COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock
RUN $HOME/.poetry/bin/poetry install
COPY . /app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]