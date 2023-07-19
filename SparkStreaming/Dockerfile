FROM bitnami/spark:latest

ADD ./ .

USER root

RUN mkdir -p /var/lib/apt/lists/partial \
    && apt-get update --fix-missing\
    && apt-get install -y python3-pip \
    && pip3 install --no-cache-dir -r requirements.txt

CMD spark-submit --master local[*] main.py

