#!bin/bash


kubectl apply -f persistent-volume.yaml
kubectl apply -f service.yaml
kubectl apply -f database.yaml
kubectl apply -f jenkins.yaml
kubectl apply -f application.yaml
