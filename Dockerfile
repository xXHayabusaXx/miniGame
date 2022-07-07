
FROM cren0/nginxflask:latest

WORKDIR /app
COPY ./app /app

CMD ["python", "/app/main.py"]

