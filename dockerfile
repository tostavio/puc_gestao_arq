FROM python:3-alpine3.11
RUN apk update && apk add --no-cache \
  build-base \
  python3-dev \
  libevent-dev \
  && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]