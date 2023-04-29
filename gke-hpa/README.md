1. Create Cluster

```bash
gcloud container clusters create deepsparse-cluster-simple \
    --min-cpu-platform="Intel Ice Lake" --machine-type=n2-highcpu-32 --threads-per-core=1 \
    --zone us-central1-a --node-locations us-central1-a \
    --num-nodes=1 
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

3. Put System Under Load

Get IP of the service:
```bash
NAME                 TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)        AGE
deepsparse-service   LoadBalancer   10.24.3.229   34.27.180.142   80:30839/TCP   48m
kubernetes           ClusterIP      10.24.0.1     <none>          443/TCP        86m
```

Put system under load:
```bash
python3 client.py --num_streams 2 --ip 34.27.180.142 --iters 1000
```

HTOP shows about 12-13% utilization on each of the 16 physical cores, which equals 2 CPUs ... so the resource limit is hit exactly (since vCPUs == physical CPUs, the autoscale metric now ties directly to physical core utilization)

Running the following shows the calculated metric is now at the resource limit / request:

```bash
kubectl top pods

NAME                                     CPU(cores)   MEMORY(bytes)   
deepsparse-deployment-5884868d45-q7hl9   1939m        808Mi 
```

4. Add HPA

```bash
kubectl apply -f hpa.yaml
```

Add more load to the system:
```bash
python3 client.py --ip 34.27.180.142 --num_streams 32 --iters 10000
```

We should see it scale up to 7 pods (then run out of space trying to create an 8th pod).

Take load off the system:
```bash
python3 client.py --ip 34.27.180.142 --num_streams 2 --iters 10000
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