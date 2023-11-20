FROM python:3.12-alpine
WORKDIR /app
COPY ./requirements.txt /app
COPY ./securities_functions/* /app/securities_functions
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8015
ENV SECURITIES_APP=app.py
CMD ["python", "app.py"]

