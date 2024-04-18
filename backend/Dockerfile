FROM python:3.10

WORKDIR /app

RUN python3 -m venv /venv

ENV PATH=/venv/bin:$PATH

COPY requirements/requirements_local.txt .

RUN apt-get update && apt-get install nano && apt-get install -y telnet

RUN pip install --upgrade pip && pip install -r requirements_local.txt --no-cache-dir

COPY . .

RUN chmod +x etrypoint.sh

ENTRYPOINT ["/app/etrypoint.sh"]