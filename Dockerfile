# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

# some packages to build the C extension
RUN apt update
RUN apt install -y g++

RUN useradd -ms /bin/bash qcaweb
USER qcaweb

ENV PATH="${PATH}:/home/qcaweb/.local/bin"

WORKDIR /home/qcaweb
COPY --chown=qcaweb:qcaweb ./ qcaweb_src

RUN python -m pip install --user --upgrade pip
RUN pip install --user ./qcaweb_src/
RUN rm -Rf qcaweb_src

CMD ["gunicorn", "-b", "0.0.0.0:8000", "qcarchive_webapps:create_app('production')"]
