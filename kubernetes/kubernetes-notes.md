# Kubernetes Notes

## Create deployment
```bash
kubectl create -f deployment-definition.yml
```

## Get deployment details
```bash
kubectl get deployments
```

## Update deployment details 
```bash
kubectl apply -f deployment-definition.yml

kubectl set image deployment/myapp-deployment nginx=nginx:1.9.1 
```

## Check rollout status 
```bash
kubectl rollout status deployment/myapp-deployment 

kubectl rollout history deployment/myapp-deployment 
```

## Rollback 
```bash
kubectl rollout undo deployment/myapp-deployment
```
