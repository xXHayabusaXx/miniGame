
FROM cren0/nginxflask:latest

WORKDIR /app
COPY ./app /app

CMD ["python", "/app/main.py"]




# ____________________________________________


#FROM python:latest


#WORKDIR /app
#COPY ./app/requirement.txt /app

# python3.9
#RUN apt update 
#RUN apt install software-properties-common -y
#RUN apt install python3.9 -y

# pip3
#RUN apt install python3-pip -y

# repo of mariadb
#RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db
#RUN curl -LsS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash

# updates
#RUN apt-get update
#RUN apt-get upgrade -y
#RUN apt-get dist-upgrade

# connector/c
#RUN apt-get install -y \
#    libmariadb3 \
#    libmariadb-dev    

# requirements
#RUN pip3 install -r requirement.txt

#EXPOSE 8080

