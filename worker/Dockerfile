FROM python:3.7.4-alpine3.10

RUN mkdir /opt/worker
WORKDIR /opt/worker
RUN apk update
RUN apk add --no-cache openssl
RUN apk add bash
RUN wget https://raw.githubusercontent.com/eficode/wait-for/master/wait-for -O /opt/wait-for.sh
RUN chmod a+x /opt/wait-for.sh
ADD ./requirements.txt /opt/worker/requirements.txt
RUN pip3 install -U pip
RUN pip install -r requirements.txt
ADD ./aggregator.py /opt/worker/aggregator.py
ADD ./worker.py /opt/worker/worker.py
ADD ./sender.py /opt/worker/sender.py
ADD ./preprocessor.py /opt/worker/preprocessor.py
CMD python3 /opt/worker/worker.py
