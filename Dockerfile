FROM python:3.9

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app/ .

EXPOSE 5000

CMD [ "python", "./app.py"]