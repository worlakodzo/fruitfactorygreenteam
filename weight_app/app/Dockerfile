FROM python:3.10
RUN apt-get update
 
RUN apt-get install -y gcc
RUN apt-get install -y default-libmysqlclient-dev
RUN pip install mysql-connector-python

WORKDIR /app

EXPOSE 5000

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

COPY . .
ENTRYPOINT [ "python3" ]
CMD ["app.py"]
