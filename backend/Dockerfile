FROM python:3.10.4-slim

LABEL author="Bykov Evgeniy" version=1 release_date=25-08-2022

WORKDIR /app

COPY . .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
