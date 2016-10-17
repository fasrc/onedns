FROM python:2.7.12-slim
MAINTAINER Harvard Unviersity Faculty of Arts and Sciences Research Computing

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
RUN pip install --no-cache-dir /usr/src/app/

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 53

ENTRYPOINT ["/usr/local/bin/onedns"]

CMD ["daemon"]
