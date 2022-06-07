FROM python:latest

RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirement.txt

EXPOSE 5000
CMD ["python", "/app/main.py"]
