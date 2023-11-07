FROM python:3.7-slim

WORKDIR /app

RUN pip install gunicorn==20.1.0

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0:8000", "foodgram.wsgi:application"]

# При старте контейнера запустить сервер разработки.
# CMD ["python", "manage.py", "runserver", "0:8000"] 
