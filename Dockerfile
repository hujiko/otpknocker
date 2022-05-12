FROM python:3.7-alpine

RUN mkdir /app
RUN mkdir /app/html
RUN mkdir /app/static
WORKDIR /app

ADD requirements.txt /app
ADD main.py /app
ADD html/* /app/html
ADD static/* /app/static

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "-w 2", "-b", "0.0.0.0:80", "main:app"]
