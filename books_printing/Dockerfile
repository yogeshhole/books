FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip3 install pipenv

WORKDIR /app/src

COPY ./Pipfile Pipfile

COPY ./Pipfile.lock Pipfile.lock

RUN set -ex && pipenv install --deploy --system --ignore-pipfile --keep-outdated

COPY ./src /app/src
