FROM python:3.9-slim

WORKDIR /app

COPY Pipfile .

COPY Pipfile.lock .

RUN python -m pip install --upgrade pip

RUN python -m pip install pipenv

ENV PIPENV_VENV_IN_PROJECT=1

RUN pipenv sync

COPY . .

# RUN pipenv run ./manage.py collectstatic --noinput
# RUN pipenv run ./manage.py migrate

EXPOSE 8000

CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi"]
