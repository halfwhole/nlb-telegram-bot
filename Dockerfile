FROM python:3.6-slim-buster
RUN pip install pipenv
WORKDIR /nlb-telegram-bot/
COPY Pipfile Pipfile.lock /nlb-telegram-bot/
RUN pipenv install
