FROM python:3.8-slim
WORKDIR /app/api_foodgram
COPY requirements.txt .
RUN pip3 install -r /app/api_foodgram/requirements.txt --no-cache-dir
COPY . /app
# CMD ["gunicorn", "api_foodgram.wsgi:application", "--bind", "0:8000"]
CMD ["python3", "manage.py", "runserver", "0:8000"]
