https://kubernetes.io/blog/2018/07/24/feature-highlight-cpu-manager/
- Enable CPU Manager with Static policy in the Kubelet
- Configure pod to be in the Guaranteed QOS (whole numbers of CPU cores, request=limit)

```bash
minikube start --extra-config=kubelet.cpu-manager-policy="static" --extra-config=kubelet.kube-reserved="cpu=500m"   --extra-config=kubelet.feature-gates="CPUManager=true" --extra-config="kubelet.cpu-manager-policy-options=full-pcpus-only=true"
```

```bash
kubectl apply -f metrics-server.yaml
```


```bash
eval $(minikube docker-env)
docker build -t deepsparse-nightly .
```

```bash
kubectl apply -f deepsparse.yaml
```

```bash
cd client
```

```bash
docker build -t client .
```

```bash
kubectl apply -f client-deployment.yaml
```

```bash
kubectl get services
NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
deepsparse-service   ClusterIP   10.111.101.158   <none>        80/TCP    6m52s
kubernetes           ClusterIP   10.96.0.1        <none>        443/TCP   28m
```

```bash
kubectl exec --stdin --tty client-deployment-59f5c555d5-8htws -- /bin/bash
```

```bash
python3 run.py --ip 10.111.101.158 --iters 10000 --num_streams 12
```

```bash
kubectl apply -f hpa.yaml
```

We should see autoscaling

```bash
Every 0.1s: kubectl get hpa; kubectl top pods; kubectl get pods                                                                                                                                  ice-lake-16-cores-minikube: Sat May  6 13:17:26 2023

NAME                    REFERENCE                          TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
deepsparse-deployment   Deployment/deepsparse-deployment   28%/30%   1         10        10         6m54s
NAME                                     CPU(cores)   MEMORY(bytes)
client-deployment-59f5c555d5-8htws       176m         14Mi
deepsparse-deployment-794566bfb7-64whd   1120m        655Mi
deepsparse-deployment-794566bfb7-cl4xq   1052m        662Mi
deepsparse-deployment-794566bfb7-kf4nx   1204m        652Mi
deepsparse-deployment-794566bfb7-nmd9v   1054m        660Mi
deepsparse-deployment-794566bfb7-q54gj   1112m        650Mi
deepsparse-deployment-794566bfb7-s4qdz   1150m        658Mi
deepsparse-deployment-794566bfb7-xw2p7   1207m        654Mi
NAME                                     READY   STATUS    RESTARTS   AGE
client-deployment-59f5c555d5-8htws       1/1     Running   0          21m
deepsparse-deployment-794566bfb7-64whd   1/1     Running   0          4m9s
deepsparse-deployment-794566bfb7-9sm26   0/1     Pending   0          2m24s
deepsparse-deployment-794566bfb7-cl4xq   1/1     Running   0          27m
deepsparse-deployment-794566bfb7-cztqw   0/1     Pending   0          2m24s
deepsparse-deployment-794566bfb7-gqlkc   0/1     Pending   0          2m24s
deepsparse-deployment-794566bfb7-kf4nx   1/1     Running   0          3m24s
deepsparse-deployment-794566bfb7-nmd9v   1/1     Running   0          4m54s
deepsparse-deployment-794566bfb7-q54gj   1/1     Running   0          3m24s
deepsparse-deployment-794566bfb7-s4qdz   1/1     Running   0          3m24s
deepsparse-deployment-794566bfb7-xw2p7   1/1     Running   0          4m9s
```
