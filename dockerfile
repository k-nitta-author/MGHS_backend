FROM python:3.12

COPY /src /src/

EXPOSE 5000

RUN pip install Flask-SQLAlchemy
RUN pip install flask
RUN pip install flask_httpauth
RUN pip install mysqlclient

CMD ["python", "./src/main.py"]