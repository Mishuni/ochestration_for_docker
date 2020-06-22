FROM python:3.6

EXPOSE 5000
ENV APP /www

RUN mkdir $APP
ADD . $APP
WORKDIR $APP

RUN python -m pip install --upgrade pip 
RUN pip3 install Flask pytz flask-mqtt flask-socketio flask-bootstrap eventlet requests flask-mongoengine

# run uWSGI with the ini file
CMD python3 /www/app.py
