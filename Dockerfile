FROM python:3.8

ENV HOME /root/web_server
WORKDIR /root/web_server

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait

RUN chmod +x /wait

ENV FLASK_APP web_server
ENV FLASK_DEBUG 1

CMD /wait && flask run