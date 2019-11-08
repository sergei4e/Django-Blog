FROM python:3

WORKDIR /code

RUN apt update

RUN apt install -y python-pil python3-pil

RUN apt install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 \
    libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 \
    fonts-liberation libappindicator3-1 libnss3 lsb-release xdg-utils libsdl1.2-dev \
    libpq-dev python3-dev

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /code

# install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

RUN chmod +x /code/run_web.sh