# Cow wisdom web server

## Prerequisites

```
sudo apt install fortune-mod cowsay -y
```

## How to use?

1. Run `./wisecow.sh`
2. Point the browser to server port (default 4499)

## What to expect?
![wisecow](https://github.com/nyrahul/wisecow/assets/9133227/8d6bfde3-4a5a-480e-8d55-3fef60300d98)

---

# 📋 Accuknox DevOps Trainee Practical Assessment

This repository contains complete implementations of all three problem statements:

## ✅ **PROBLEM STATEMENT 1: Containerization & Deployment**

**Objective:** Containerize and deploy Wisecow application on Kubernetes with secure TLS communication.

**Deliverables:**
- `Dockerfile` - Container image with Ubuntu 22.04, fortune-mod, cowsay, netcat-openbsd
- `k8s-deployment.yaml` - Kubernetes deployment with 2 replicas, health checks, resource limits
- `k8s-service.yaml` - ClusterIP service exposing port 80 → 4499
- `k8s-ingress.yaml` - NGINX ingress with TLS support
- `k8s-cert-issuer.yaml` - Let's Encrypt ACME certificate issuer for automatic TLS
- `.github/workflows/build-and-deploy.yaml` - GitHub Actions CI/CD pipeline
- `DEPLOYMENT.md` - Complete deployment guide with troubleshooting

**Features:**
- ✅ Multi-replica deployment for high availability
- ✅ Automatic TLS/HTTPS with cert-manager
- ✅ Health checks (liveness & readiness probes)
- ✅ Automated CI/CD with GitHub Actions
- ✅ GitHub Container Registry integration

---

## ✅ **PROBLEM STATEMENT 2: System Monitoring Scripts**

**Objective:** Implement two monitoring scripts using Python to track system health and application availability.

**Deliverables:**
- `system_health_monitor.py` - System health monitoring script
  - CPU usage monitoring (threshold: 80%)
  - Memory usage monitoring (threshold: 80%)
  - Disk space monitoring (threshold: 80%)
  - Running processes monitoring (threshold: 100)
  - Top 5 processes by CPU and memory
  - File and console logging

- `app_health_checker.py` - Application health checker script
  - HTTP endpoint availability checking
  - Status code validation
  - Retry logic (3 attempts with 2-second delays)
  - JSON output for integration
  - Detailed error handling

**Features:**
- ✅ Production-ready Python code
- ✅ Comprehensive error handling
- ✅ Structured logging
- ✅ Exit codes for automation

---

## ✅ **PROBLEM STATEMENT 3: KubeArmor Zero-Trust Policy**

**Objective:** Write a zero-trust KubeArmor policy for the Kubernetes workload deployed in PS1.

**Deliverables:**
- `kubearmor-policy.yaml` - Zero-trust security policy
  - Process execution whitelist: bash, sh, wisecow.sh, fortune, cowsay, nc, sleep
  - File access control: Read-only for system dirs, write to /tmp
  - Network restrictions: Inbound TCP 4499, outbound UDP 53 (DNS)
  - Audit mode for safe testing

- `KUBEARMOR_GUIDE.md` - KubeArmor setup and monitoring guide
  - Installation instructions
  - Policy deployment guide
  - Violation monitoring
  - Switching between Audit and Enforce modes

**Features:**
- ✅ Process execution whitelist
- ✅ File access restrictions
- ✅ Network policy enforcement
- ✅ Audit mode for safe testing
- ✅ Easy switch to enforce mode

---

## 📚 Documentation

- **DEPLOYMENT.md** - Complete Kubernetes deployment guide
- **KUBEARMOR_GUIDE.md** - KubeArmor installation and policy deployment guide

## 🚀 Quick Start

### Problem Statement 1: Deploy Wisecow
```bash
docker build -t wisecow:latest .
kind load docker-image wisecow:latest
kubectl apply -f k8s-cert-issuer.yaml
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml
kubectl apply -f k8s-ingress.yaml
```

### Problem Statement 2: Run Monitoring Scripts
```bash
python3 system_health_monitor.py
python3 app_health_checker.py
```

### Problem Statement 3: Deploy KubeArmor Policy
```bash
helm install kubearmor kubearmor/kubearmor -n kubearmor --create-namespace
kubectl apply -f kubearmor-policy.yaml
```

---

## 📊 Original Problem Statement

Deploy the wisecow application as a k8s app

### Requirement
1. Create Dockerfile for the image and corresponding k8s manifest to deploy in k8s env. The wisecow service should be exposed as k8s service.
2. Github action for creating new image when changes are made to this repo
3. [Challenge goal]: Enable secure TLS communication for the wisecow app.

### Expected Artifacts
1. Github repo containing the app with corresponding dockerfile, k8s manifest, any other artifacts needed.
2. Github repo with corresponding github action.
3. Github repo should be kept private and the access should be enabled for following github IDs: nyrahul
