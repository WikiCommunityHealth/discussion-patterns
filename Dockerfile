FROM python:3.8.5

WORKDIR /usr/src/app

RUN pip install poetry==1.0.0

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

COPY . /code

CMD [ "python", "./test.py" ]