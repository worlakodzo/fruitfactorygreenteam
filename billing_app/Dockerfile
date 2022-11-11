FROM python:3.8.5-alpine
#FROM python:3.12.0a1-alpine3.15

WORKDIR /app
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=127.0.0.1
RUN python -m pip install --upgrade pip

EXPOSE 5000

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]
