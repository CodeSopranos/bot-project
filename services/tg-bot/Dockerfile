FROM python:slim

WORKDIR /usr/src/tg-bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt  /usr/src/app/requirements.txt
RUN pip install -r  /usr/src/app/requirements.txt

COPY . /usr/src/tg-bot/


EXPOSE 8081

CMD ["python", "main.py"]