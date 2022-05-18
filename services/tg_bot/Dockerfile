FROM python:3.8

WORKDIR /usr/src/tg_bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt  /usr/src/app/requirements.txt
RUN pip install -r  /usr/src/app/requirements.txt

COPY . /usr/src/tg_bot/


EXPOSE 8081

CMD ["python", "run.py"]