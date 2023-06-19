FROM python:3.9-slim-bullseye

WORKDIR /app

COPY entrypoint.sh /home/docker/entrypoint.sh
COPY requirements.txt .

RUN pip install --upgrade pip --default-timeout=100
RUN pip install -r requirements.txt --no-cache-dir --default-timeout=100

COPY . .

CMD ["/home/docker/entrypoint.sh"]