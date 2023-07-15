FROM python:3.9-slim

ADD requirements.txt .

RUN apt-get -y update
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ADD src/ .

EXPOSE 4555

CMD ["python", "app.py"]