#!/bin/bash

kubectl apply -f kubernetes/huey-worker-deployment.yaml
kubectl apply -f kubernetes/redis-huey-service.yaml
kubectl apply -f kubernetes/redis-kv-deployment.yaml
kubectl apply -f kubernetes/fastapi-deployment.yaml
kubectl apply -f kubernetes/redis-kv-service.yaml
kubectl apply -f kubernetes/fastapi-service.yaml
kubectl apply -f kubernetes/redis-huey-deployment.yaml

echo "Deployment completed."
