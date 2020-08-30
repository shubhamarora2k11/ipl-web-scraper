FROM ubuntu:latest
MAINTAINER Shubham "shubhamarora2k11@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN apt-get install -y git

RUN mkdir /code
WORKDIR /code
RUN git clone https://github.com/shubhamarora2k11/ipl-web-scraper.git
RUN pip install -r ipl-web-scraper/requirements.txt

CMD ["python3","ipl-web-scraper/scraper.py"]
