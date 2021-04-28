FROM python:3.6-slim

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends
RUN apt-get install -y ffmpeg

# Torch and dependencies:
WORKDIR /requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Python server requirements
COPY server/requirements.txt .server-requirements.txt
RUN pip install -r .server-requirements.txt

WORKDIR /