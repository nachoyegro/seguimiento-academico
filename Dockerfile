FROM python:3.8.0-alpine
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add bash postgresql-dev gcc python3-dev musl-dev

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN python alumnos/manage.py collectstatic
CMD ["gunicorn", "--timeout", "1800", "-w", "1", "-b", ":8001", "--pythonpath", "alumnos", "--env", "DJANGO_SETTINGS_MODULE=alumnos.settings", "alumnos.wsgi:application"]
