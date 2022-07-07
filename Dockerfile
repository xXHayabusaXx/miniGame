
FROM cren0/nginxflask:latest

WORKDIR /app
COPY ./miniGame/app /app

CMD ["python", "/app/main.py"]


