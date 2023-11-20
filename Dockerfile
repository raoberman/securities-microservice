FROM python:3.12.0-slim-bookworm

WORKDIR /app

COPY ./requirements.txt /app

COPY ./securities_functions/* /app/securities_functions/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8015
ENV SECURITIES_APP=app.py
CMD ["python", "app.py"]

