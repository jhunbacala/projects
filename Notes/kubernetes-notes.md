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

## How to scale replicas on the fly 
```bash
kubectl scale deployment vote --replicas=5
```


## How to get the service port when running Minikune on Docker Desktop
```bash
minikube service <service-name>
```

## Why the Nodeport is not accessible when running Minikube on Docker Desktop.
The internal IP (192.168.49.2) you're seeing is the Minikube VM's IP, which is typically not directly accessible or pingable from your macOS host when using the default Docker driver. This is due to how the networking is set up—Minikube runs inside a containerized environment within Docker Desktop's VM, limiting direct host-to-VM connectivity for services like NodePort. Direct browser access to 192.168.49.2:31000 won't work without additional setup.
To access your NodePort service (assuming it's named something like my-service; replace with your actual service name):

Run `minikube service my-service` in your terminal. This will automatically open the service in your default browser via a local tunnel (e.g., forwarding to something like `http://127.0.0.1:<random-port>`).
If you prefer to get the URL without opening the browser, use `minikube service my-service --url`. This will output a local URL (again, like `http://127.0.0.1:<random-port>`). Keep this terminal window open to maintain the tunnel—closing it will terminate the access. You can then paste the URL into your browser.

If the service still doesn't load:

Verify the service is running correctly: `kubectl get svc my-service` (check the NodePort is indeed 31000 and the selector matches your pods).
Check pod status: `kubectl get pods` and `kubectl describe pod <pod-name>` for any errors.
Ensure Minikube is healthy: minikube status.
If using an Apple Silicon Mac (M1/M2), confirm your driver with minikube config get driver. If it's docker and issues persist, try switching to qemu for better networking: Stop Minikube (`minikube stop`), then restart with `minikube start --driver=qemu`. Note that qemu may require additional setup like installing QEMU via Homebrew.

This approach uses Minikube's built-in tunneling to bypass the direct IP access limitation. If your setup involves a different driver or more details (e.g., service YAML), provide them for further troubleshooting.


