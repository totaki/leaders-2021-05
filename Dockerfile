FROM node:12.22-buster as frontend
RUN mkdir /app
WORKDIR /app
COPY ./frontend/yarn.lock /app/yarn.lock
COPY ./frontend/package.json /app/package.json
RUN yarn
COPY ./frontend /app
RUN yarn build

FROM nginx/unit:1.25.0-python3.9 as api
RUN mkdir /app
WORKDIR /app

RUN apt update
RUN apt install -y libpq-dev curl gcc gdal-bin
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
COPY ./backend/poetry.toml /app/poetry.toml
COPY ./backend/pyproject.toml /app/pyproject.toml
COPY ./backend/poetry.lock /app/poetry.lock
RUN $HOME/.poetry/bin/poetry install
COPY ./backend /app
RUN python manage.py collectstatic --noinput
COPY --from=frontend /app/dist/ /app/frontend_build/
