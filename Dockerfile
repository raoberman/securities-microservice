FROM public.ecr.aws/docker/library/python:3.12

RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev
RUN pip install --upgrade cython


WORKDIR /app

COPY ./requirements.txt /app

COPY ./securities_functions/* /app/securities_functions/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8015
ENV SECURITIES_APP=app.py
CMD ["python", "app.py"]

