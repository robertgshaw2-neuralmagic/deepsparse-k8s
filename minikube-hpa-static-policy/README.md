## Setup Cluster with Metrics Server Running

Create Cluster:

```bash
minikube start
```

Point shell to minikube docker:

```bash
eval $(minikube docker-env)
```

Download Metrics Server Manifest and Edit To Disable Certificate Authority (note: this file is already included in the directory):
```bash
wget -o metrics-server.yaml https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

https://github.com/kubernetes-sigs/metrics-server

Add `--kubelet-insecure-tls` to Metrics Server yaml

## Launch DeepSparse with HPA

Build the docker image:
```bash
docker build -t deepsparse .
```

Apply the manifest for the deployment / service:
```bash
kubectl apply -f deepsparse.yaml
```

Apply the mainfest for the hpa:
```bash
kubectl apply -f hpa.yaml
```

Check to see the hpa is active:
```bash
kubectl get hpa deepsparse-deployment
```

## Put the System Under Load

Build client docker image:

```bash
cd client
docker build -t .
cd ..
```

Add the client to the deploment:
```bash
kubectl apply -f client/deployment.yaml
```

Get client pod name:
```bash
kubectl get pods
```

Exec into the client:
```bash
kubectl exec --stdin --tty <client-pod-name> -- /bin/bash
```

Get the service Internal IP:
```bash
kubectl get services
```

Run the client load script:
```bash
python3 run.py --ip [service-ip] --num_streams 1 --iterations 1000
```

Watch the load + scaling:
```bash
watch -n0.1 "kubectl get hpa && kubectl top pod && kubectl get pods"
```

## Key Next Steps

- expand to scale nodes up
- expands to multi-region / multi-zone
- add static cpu management policy (to isolate deepsparse) - right now performance will be horrible
- check out what CPU utilization looks like under static policy (given we will maximum utilize 50% since we only use one hyperthread)
