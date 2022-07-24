FROM python:3.10

RUN apt update -y && apt upgrade -y
#RUN apt-get -y install cron

RUN apt install postgresql postgresql-contrib -y

COPY ./src /src
COPY ./requirements.txt /tmp/requirements.txt

WORKDIR /src/django_proj

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r /tmp/requirements.txt

# RUN python3 manage.py makemigrations
# RUN python3 manage.py migrate
# RUN python3 manage.py collectstatic

#RUN crontab cron
#RUN touch /tmp/out.log

CMD python3 manage.py runserver 0.0.0.0:8000
#&& cron && tail -f /tmp/out.log


