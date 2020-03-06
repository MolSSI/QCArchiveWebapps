FROM continuumio/miniconda3

LABEL MAINTAINER="Doaa Altarawy <doaa.altarawy@gmail.com>"

# replace shell with bash so we can source files
#RUN rm /bin/sh && ln -s /bin/bash /bin/sh

ENV GROUP_ID=1000 \
    USER_ID=1000
#    GIT_COMMIT=$(git rev-parse --short=8 HEAD)
# use in sh file to tag images and push them to registery

WORKDIR /var/www/

ADD ./requirements/. /var/www/requirements/
ADD ./package.json /var/www/package.json


# what's only needed for continuumio/miniconda3
RUN apt-get update && \
    pip install --upgrade pip && \
    apt-get install -y --no-install-recommends npm && \
    rm -rf /var/lib/apt/lists/*  && \
    npm install && \
    # Python
    conda install -c rdkit rdkit  && \
    pip install --no-cache-dir -r requirements/docker.txt && \
    pip install --no-cache-dir gunicorn  && \
    conda clean -y --all

ADD . /var/www/

RUN groupadd -g $GROUP_ID www  && \
    useradd -r -g www -s /bin/sh -u $USER_ID www  && \
    chown -R www:www /var/www  && \
    chown -R www:www /opt/conda/lib/python*/site-packages/qc_time_estimator

USER www

#RUN flask db upgrade

# Listens on port, doesn't publish it. Publish by -p or ports in docker-compose
EXPOSE 5000

# Run in Exec form, can't be overriden
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:5000", "qcarchive_web:app"]
# Params to pass to ENTRYPOINT, and can be overriden when running containers
CMD ["-w", "2", "--access-logfile", "access.log", "--error-logfile", "error.log"]

# can't override ENTRYPOINT shell form
#ENTRYPOINT gunicorn --bind :5000 --access-logfile - --error-logfile - qcarchive_web:app
