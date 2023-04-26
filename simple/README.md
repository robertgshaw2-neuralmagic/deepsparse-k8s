Set the project id:
```bash
export PROJECT_ID=$(gcloud config get-value project)
```

### Put Image In Artifact Repo

Run the following to build the docker container:
```bash
simple % docker build -t us-central1-docker.pkg.dev/$PROJECT_ID/deepsparse-server/sentiment-analysis:0.1 .
```

Create Artifact Repo on GCP Console.

Authenticate to Artifact Repo:

```bash
gcloud auth configure-docker us-central1-docker.pkg.dev
```

Push Container to Artifact Repo:
```bash
docker push us-central1-docker.pkg.dev/$PROJECT_ID/deepsparse-server/sentiment-analysis:0.1
```
