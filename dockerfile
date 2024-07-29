FROM python:3.12

ADD main.py .

EXPOSE 5000

RUN pip install Flask-SQLAlchemy
RUN pip install flask


CMD [ "python", "./main.py"]