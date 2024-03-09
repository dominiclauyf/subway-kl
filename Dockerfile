FROM tensorflow/tensorflow:latest-gpu
WORKDIR /subway-kl
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /subway-kl/

RUN pip install -r  requirements.txt
