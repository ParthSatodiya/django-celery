FROM python:3.6-slim
WORKDIR /code
COPY requirements.txt /tmp/pip-tmp/
RUN apt-get update \
    && pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp \
