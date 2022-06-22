
FROM nginxflask:latest

WORKDIR /app
COPY ./app /app


#EXPOSE 8080

CMD ["python", "/app/main.py"]




# ____________________________________________


#FROM python:latest


#WORKDIR /app
#COPY ./app/requirement.txt /app

#RUN apt update && apt install -y \
#    pip \
#    libmariadb3 \
#    libmariadb-dev
    
#RUN python3 -m pip install --upgrade pip
    

#RUN pip install -r requirement.txt

#EXPOSE 8080

