FROM python:3.12

ADD main.py .

EXPOSE 5000

RUN pip install Flask-SQLAlchemy
RUN pip install flask
RUN pip install flask_httpauth

CMD [ "python", "./main.py"]