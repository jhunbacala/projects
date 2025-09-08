# Troubleshooting Minikube and Kubernetes Deployment

This document logs the steps taken to troubleshoot and resolve issues with Minikube and deploying Kubernetes resources.

## 1. Initial Status Check

The first step was to check the status of Minikube.

```bash
minikube status
```

The output showed that the `apiserver` was `Stopped`, which was the root cause of the problem.

## 2. Attempted Restart

An attempt was made to restart Minikube to fix the issue.

```bash
minikube stop && minikube start
```

This command failed, indicating a more persistent problem.

## 3. Cluster Reset

To resolve the persistent issue, the Minikube cluster was deleted and recreated.

```bash
minikube delete
minikube start
```

This successfully created a new, healthy Minikube cluster.

## 4. Deploying Kubernetes Resources

With the cluster running, the Kubernetes resources were deployed.

### 4.1. Nginx Pod

The Nginx pod was deployed from the `pods/nginx.yml` file.

```bash
kubectl apply -f pods/nginx.yml
```

### 4.2. Replicaset

The replicaset was deployed from the `replicasets/replicaset.yml` file.

```bash
kubectl apply -f replicasets/replicaset.yml
```

## 5. Verifying the Deployment

After deploying the resources, their status was checked to ensure everything was running correctly.

```bash
kubectl get all
```

The output confirmed that the `nginx` pod and all replicas of the `myapp-replicaset` were in the `Running` state.
