#!bin/bash


#minikube image rm anog:latest #docker.io/library/anog:latest

#kubectl delete pod anog-cont
#minikube image build -t anog:latest -f ./Dockerfile .
#bash start.sh


#kubectl delete pod anog-cont
#bash start.sh



#kubectl delete pod anog-cont
#minikube image build -t nginxflask:latest -f ./Dockerfile .


#kubectl delete pod anog-cont
#minikube image build -t anog:latest -f ./Dockerfile .
#bash start.sh



curl -I http://admin:admin@192.168.49.2:30037/job/python-pipeline/build?token=copyCode
kubectl delete pod anog-cont
kubectl apply -f application.yaml








