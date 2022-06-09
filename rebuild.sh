#!bin/bash


kubectl delete pod anog-cont
#minikube image rm anog:latest #docker.io/library/anog:latest
minikube image build -t anog:latest -f ./Dockerfile .
bash start.sh
