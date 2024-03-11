FROM tensorflow/tensorflow:latest-gpu
WORKDIR /subway-kl
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /subway-kl/

RUN pip install -r  requirements.txt

RUN apt-get update && apt-get install -y wget

# Download the BERT model files
RUN python -c "from transformers import pipeline; pipeline('question-answering',model='bert-large-uncased-whole-word-masking-finetuned-squad')"

COPY . .
RUN  ./manage.py migrate

EXPOSE 8000
