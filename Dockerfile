FROM python:3.10.7
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /ml_bot/requirements.txt
WORKDIR /ml_bot
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .