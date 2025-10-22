# Wisecow Kubernetes Deployment Guide

This guide provides instructions for deploying the Wisecow application on Kubernetes with TLS support and CI/CD automation.

## Prerequisites

- Docker installed locally
- Kubernetes cluster (Kind, Minikube, or cloud-based)
- kubectl configured to access your cluster
- Helm (for cert-manager installation)
- NGINX Ingress Controller
- cert-manager for TLS certificate management

## Local Setup

### 1. Build Docker Image

```bash
docker build -t wisecow:latest .
```

### 2. Load Image into Kubernetes (for local clusters like Kind/Minikube)

```bash
# For Kind
kind load docker-image wisecow:latest

# For Minikube
minikube image load wisecow:latest
```

## Kubernetes Deployment

### 1. Install NGINX Ingress Controller

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml
```

### 2. Install cert-manager

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --set installCRDs=true
```

### 3. Apply ClusterIssuer for TLS

```bash
kubectl apply -f k8s-cert-issuer.yaml
```

### 4. Deploy Wisecow Application

```bash
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml
kubectl apply -f k8s-ingress.yaml
```

### 5. Verify Deployment

```bash
# Check deployment status
kubectl get deployment wisecow
kubectl get pods -l app=wisecow

# Check service
kubectl get svc wisecow-service

# Check ingress
kubectl get ingress wisecow-ingress

# Check certificate status
kubectl get certificate
```

## Accessing the Application

### Local Testing (Kind/Minikube)

For local clusters, add the following to your `/etc/hosts`:

```
127.0.0.1 wisecow.local
```

Then access: `https://wisecow.local`

### Port Forwarding

```bash
kubectl port-forward svc/wisecow-service 8080:80
```

Access: `http://localhost:8080`

## CI/CD Pipeline

The GitHub Actions workflow automatically:

1. Builds the Docker image on every push to main/master
2. Pushes the image to GitHub Container Registry (GHCR)
3. Deploys the updated image to the Kubernetes cluster

### Required Secrets

Add the following secrets to your GitHub repository:

- `KUBE_CONFIG`: Base64-encoded kubeconfig file for your cluster

```bash
cat ~/.kube/config | base64 | pbcopy
```

## Troubleshooting

### Certificate Not Issuing

```bash
kubectl describe certificate wisecow-tls-cert
kubectl describe clusterissuer letsencrypt-prod
```

### Pod Not Starting

```bash
kubectl logs -l app=wisecow
kubectl describe pod <pod-name>
```

### Ingress Not Working

```bash
kubectl describe ingress wisecow-ingress
kubectl get events
```

## Cleanup

```bash
kubectl delete -f k8s-ingress.yaml
kubectl delete -f k8s-service.yaml
kubectl delete -f k8s-deployment.yaml
```

