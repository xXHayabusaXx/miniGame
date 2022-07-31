#!/bin/bash


kubectl delete pod mariadb-anog
kubectl delete pod anog-cont

kubectl delete svc jenkins-service
kubectl delete svc mariadb-anog-service
kubectl delete svc anog


#kubectl delete pvc anog-pvc
#kubectl delete pvc code-anog-pvc


#kubectl delete pv anog-volume
#kubectl delete pv code-anog-volume