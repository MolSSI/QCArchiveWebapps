FROM continuumio/miniconda3

LABEL MAINTAINER="Doaa Altarawy <doaa.altarawy@gmail.com>"


ENV GROUP_ID=1000 \
    USER_ID=1000
#    GIT_COMMIT=$(git rev-parse --short=8 HEAD)
# use in sh file to tag images and push them to registery
# not tested to work here

WORKDIR /var/www/

ADD ./requirements/. /var/www/requirements/
ADD ./package.json /var/www/package.json

# what's only needed for continuumio/miniconda3
RUN pip install --no-cache-dir -r requirements/docker.txt \
    && pip install --no-cache-dir gunicorn \
    && conda clean -y --all \
    && apt update \
    && apt-get install -y --no-install-recommends npm \
    && rm -rf /var/lib/apt/lists/*  \
    && npm install

ADD . /var/www/

RUN groupadd -g $GROUP_ID www \
    && useradd -r -g www -s /bin/sh -u $USER_ID www \
    && chown -R www:www /var/www

USER www

#RUN flask db upgrade

# Listens on port, doesn't publish it. Publish by -p or ports in docker-compose
EXPOSE 5000

# Run in Exec form, can't be overriden
ENTRYPOINT [ "gunicorn", "-w", "1", "--bind", "0.0.0.0:5000", "qcarchive_web:app"]
# Params to pass to ENTRYPOINT, and can be overriden when running containers
CMD ["--access-logfile", "-", "--error-logfile", "-"]

# can't override ENTRYPOINT shell form
#ENTRYPOINT gunicorn --bind :5000 --access-logfile - --error-logfile - qcarchive_web:app
