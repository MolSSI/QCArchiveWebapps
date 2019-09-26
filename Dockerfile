FROM python:3.6-alpine

ENV FLASK_APP qcarchive_web.py
ENV FLASK_CONFIG production

RUN adduser -D qcarchive
USER flasky

WORKDIR /home/qcarchive_web

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY migrations migrations
COPY qcarchive_web.py config.py boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
