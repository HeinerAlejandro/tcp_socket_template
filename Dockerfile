FROM python:3.11-slim-bullseye AS base

LABEL MAINTAINER="heiner.enis@gmail.com" \
      description="This server handle request from socket clients and get data from S3 http server"

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

COPY ./config.yaml /config.yaml

FROM base AS python-deps

RUN python3 -m venv /.venv

COPY ./requirements.txt /requirements.txt

RUN /.venv/bin/pip install -r requirements.txt

FROM base AS runtime

COPY . .

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python

USER 999

EXPOSE 5000/tcp

CMD ["python", "main.py"]