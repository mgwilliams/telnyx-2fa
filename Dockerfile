FROM python:3.8-alpine

ENV APP telnyx-2fa
WORKDIR $APP

RUN apk add -U --no-cache make g++ libffi-dev python3-dev
RUN pip install -I -U pip setuptools wheel

COPY . /$APP

RUN pip install -r requirements.txt
RUN pip install . ./telnyx-python

EXPOSE 80

ENTRYPOINT ["./entry.py"]
