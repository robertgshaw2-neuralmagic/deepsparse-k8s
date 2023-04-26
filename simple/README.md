## Start Cluster

Create Cluster:

```bash
minikube start
```

## Build Image

Point shell to minikube docker-daemon:

```bash
eval $(minikube -p minikube docker-env)
```

Run the following to build the docker image:
```bash
docker build -t deepsparse/sentiment-analysis .
```

Create the deployment:
```bash
kubectl apply -f deployment.yaml
```


https://kubernetes.io/blog/2018/07/24/feature-highlight-cpu-manager/

- Enable CPU Manager with Static policy in the Kubelet
- Configure pod to be in the Guaranteed QOS (whole numbers of CPU cores, request=limit)

```bash
minikube start --extra-config=kubelet.cpu-manager-policy="static" --extra-config=kubelet.kube-reserved="cpu=500m"   --extra-config=kubelet.feature-gates="CPUManager=true" --extra-config="kubelet.cpu-manager-policy-options=full-pcpus-only=true"
```
