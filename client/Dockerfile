FROM python:3.6

EXPOSE 5000
ENV APP /client
ENV DEVICENAME 'teamgold'

RUN mkdir $APP
ADD . $APP
WORKDIR $APP

RUN python -m pip install --upgrade pip 
RUN pip3 install requests paho-mqtt simplejson
#docker run --name test4 -e DEVICENAME='teamTest' client:test3
CMD python3 /client/client_server.py

