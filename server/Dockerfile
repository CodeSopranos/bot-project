FROM python:slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt  /usr/src/app/requirements.txt
RUN pip install -r  /usr/src/app/requirements.txt

COPY . /usr/src/app/


EXPOSE 8000

# CMD ["python", "run.py"]
CMD [ "uvicorn" , "run:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]