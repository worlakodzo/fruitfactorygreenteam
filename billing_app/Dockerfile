FROM python:3.8.5-alpine
#FROM python:3.12.0a1-alpine3.15

WORKDIR /app

EXPOSE 5000

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]
