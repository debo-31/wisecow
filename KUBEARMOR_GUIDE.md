# KubeArmor Zero-Trust Policy Guide for Wisecow

This guide provides instructions for deploying and managing KubeArmor security policies for the Wisecow application.

## What is KubeArmor?

KubeArmor is a container and Kubernetes security engine that restricts the behavior of containers at runtime. It provides:
- Process execution control
- File access restrictions
- Network policy enforcement
- Capability restrictions
- Syscall filtering

## Prerequisites

- Kubernetes cluster (1.16+)
- kubectl configured
- Helm (optional, for easier installation)
- Linux kernel with eBPF support (5.8+)

## Installation

### 1. Install KubeArmor

Using Helm:
```bash
helm repo add kubearmor https://kubearmor.github.io/charts
helm repo update
helm install kubearmor kubearmor/kubearmor -n kubearmor --create-namespace
```

Or using kubectl:
```bash
kubectl apply -f https://raw.githubusercontent.com/kubearmor/KubeArmor/main/deployments/kubernetes/kubearmor.yaml
```

### 2. Verify Installation

```bash
kubectl get pods -n kubearmor
kubectl get daemonset -n kubearmor
```

### 3. Install KubeArmor CLI (karmor)

```bash
curl -s https://raw.githubusercontent.com/kubearmor/KubeArmor/main/install.sh | sudo bash
```

## Deploying the Wisecow Policy

### 1. Apply the KubeArmorPolicy

```bash
kubectl apply -f kubearmor-policy.yaml
```

### 2. Verify Policy Deployment

```bash
kubectl get kubearmor policies
kubectl describe kubearmor wisecow-zero-trust-policy
```

### 3. Check Policy Status

```bash
karmor policy list
karmor policy get wisecow-zero-trust-policy
```

## Policy Details

The `kubearmor-policy.yaml` implements a zero-trust security model with:

### Process Restrictions
- Only allows: bash, sh, wisecow.sh, fortune, cowsay, nc, sleep
- Denies all other process executions

### File Access Control
- Read-only access to: /app, /usr/bin, /usr/share, /etc, /lib, /lib64, /proc, /dev
- Write access to: /tmp
- Denies all other file operations

### Network Restrictions
- Allows inbound TCP on port 4499 (Wisecow service)
- Allows outbound UDP on port 53 (DNS)
- Denies all other network access

## Monitoring Policy Violations

### 1. View Audit Logs

```bash
# Using karmor CLI
karmor log

# Using kubectl logs
kubectl logs -n kubearmor -l app=kubearmor -f

# Using journalctl (on nodes)
sudo journalctl -u kubearmor -f
```

### 2. Check Violations for Wisecow Pod

```bash
# Get pod name
POD_NAME=$(kubectl get pods -l app=wisecow -o jsonpath='{.items[0].metadata.name}')

# View logs for that pod
kubectl logs $POD_NAME
```

### 3. Real-time Monitoring

```bash
# Watch for policy violations
karmor log --filter=policy=wisecow-zero-trust-policy

# Filter by action
karmor log --filter=action=Deny
```

## Switching from Audit to Enforce Mode

To switch from Audit (logging only) to Enforce (blocking violations):

```bash
kubectl patch kubearmor wisecow-zero-trust-policy --type='json' \
  -p='[{"op": "replace", "path": "/spec/action", "value":"Block"}]'
```

**Warning**: Only switch to Enforce mode after thoroughly testing in Audit mode.

## Troubleshooting

### Policy Not Applied

```bash
# Check if KubeArmor is running
kubectl get pods -n kubearmor

# Check policy syntax
kubectl apply -f kubearmor-policy.yaml --dry-run=client

# Check events
kubectl describe kubearmor wisecow-zero-trust-policy
```

### No Violations Detected

1. Verify the policy selector matches the pod labels:
```bash
kubectl get pods -l app=wisecow --show-labels
```

2. Check if KubeArmor is monitoring the pod:
```bash
karmor vm list
```

3. Verify the pod is running:
```bash
kubectl get pods -l app=wisecow
```

### High Volume of Violations

If you see too many violations:
1. Review the policy rules
2. Add more Allow rules for legitimate operations
3. Check if the application behavior has changed

## Example Violations

Common violations you might see:

1. **Process Execution**: Attempting to run unauthorized commands
```
Process: /bin/bash -c "unauthorized_command"
Action: Deny
```

2. **File Access**: Attempting to write to restricted directories
```
File: /etc/passwd
Operation: Write
Action: Deny
```

3. **Network Access**: Attempting to connect to unauthorized ports
```
Network: 192.168.1.100:9999
Protocol: TCP
Action: Deny
```

## Best Practices

1. **Start in Audit Mode**: Always start with Audit mode to understand application behavior
2. **Gradual Enforcement**: Gradually move to Enforce mode after testing
3. **Regular Reviews**: Regularly review logs for unexpected patterns
4. **Update Policies**: Update policies when application requirements change
5. **Document Changes**: Document all policy changes and reasons

## References

- [KubeArmor Documentation](https://docs.kubearmor.io/)
- [KubeArmor GitHub](https://github.com/kubearmor/KubeArmor)
- [KubeArmor Policy Specification](https://docs.kubearmor.io/kubearmor/policy_language)

