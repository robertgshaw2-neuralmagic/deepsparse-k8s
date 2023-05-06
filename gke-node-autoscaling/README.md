1. Create Cluster

```bash
gcloud container clusters create deepsparse-cluster-simple \
    --min-cpu-platform="Intel Ice Lake" --machine-type=n2-highcpu-16 --threads-per-core=1 \
    --zone us-central1-a --node-locations us-central1-a \
    --num-nodes=1 \
    --enable-autoscaling --min-nodes=1 --max-nodes=4
```

2. Build and Push Container to Aritfact Repo

Create Artifact Repository called `deepsparse-cluster-simple-repo`

Set env variable:
```bash
export PROJECT_ID=$(gcloud config get-value project)
```

Build container:
```bash
docker build -t us-central1-docker.pkg.dev/$PROJECT_ID/deepsparse-cluster-simple-repo/deepsparse .
```

Push container:
```bash
docker push us-central1-docker.pkg.dev/$PROJECT_ID/deepsparse-cluster-simple-repo/deepsparse
```

Build client:
```bash
docker build -t us-central1-docker.pkg.dev/$PROJECT_ID/deepsparse-cluster-simple-repo/client .
```

Push container:
```bash
docker push us-central1-docker.pkg.dev/$PROJECT_ID/deepsparse-cluster-simple-repo/client
```

2. Launch Service

```bash
kubectl apply -f deepsparse.yaml
```

Get IP of the service:
```bash
kubectl get services

NAME                 TYPE           CLUSTER-IP    EXTERNAL-IP    PORT(S)        AGE
deepsparse-service   LoadBalancer   10.24.1.252   34.72.111.81   80:30408/TCP   2m56s
kubernetes           ClusterIP      10.24.0.1     <none>         443/TCP        8m46s
```

3. Scale Up 

Put system under load:
```bash
python3 client.py --num_streams 128 --ip 34.72.111.81 --iters 10000
```

```bash
kubectl top nodes

NAME                                                  CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
gke-deepsparse-cluster-s-default-pool-4f88feb5-fwbs   117m         1%     1421Mi          10%       
gke-deepsparse-cluster-s-default-pool-4f88feb5-hr3w   6101m        77%    3249Mi          24%  
```

```bash
kubectl top pods
NAME                                     CPU(cores)   MEMORY(bytes)   
deepsparse-deployment-5884868d45-2jb5b   2013m        766Mi           
deepsparse-deployment-5884868d45-4bmcl   1990m        777Mi           
deepsparse-deployment-5884868d45-8xwlr   73m          765Mi           
deepsparse-deployment-5884868d45-vj6hx   1972m        780Mi  
```

Take load off the system:
```bash
python3 client.py --num_streams 2 --ip 34.72.111.81 --iters 1000
```

We should see utilization drop quite a bit.
```bash
kubectl get hpa

NAME                    REFERENCE                          TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
deepsparse-deployment   Deployment/deepsparse-deployment   20%/70%   1         8         8          19m
```

Eventually, the number of pods will scale down.

```bash
kubectl get hpa

NAME                    REFERENCE                          TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
deepsparse-deployment   Deployment/deepsparse-deployment   45%/70%   1         8         3          24m
NAME                                     CPU(cores)   MEMORY(bytes)
deepsparse-deployment-5884868d45-nczzc   742m         799Mi
deepsparse-deployment-5884868d45-q7hl9   846m         808Mi
deepsparse-deployment-5884868d45-t25fz   1186m        798Mi
```

https://cloud.google.com/architecture/distributed-load-testing-using-gke