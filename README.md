# SMS Spam Classifier — End-to-End MLOps

A starter project for Experiment 8. It builds an SMS spam classifier and provides ETL,
model training, MLflow tracking, tests, Streamlit UI, Docker, Kubernetes, Terraform,
and Prometheus/Grafana configuration.

## 1. Requirements
- Python 3.10–3.12 recommended
- Git
- Docker Desktop (for Docker/Kubernetes steps)
- Terraform (for the Terraform step)
- kubectl (for Kubernetes)
- Optional: MLflow UI, Prometheus and Grafana

## 2. Setup on macOS
```bash
cd spam-classifier
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

## 3. Download the dataset
```bash
python -m src.download_data
```
This downloads the UCI SMS Spam Collection dataset into `datasets/spam.csv`.
The script also supports a local CSV with columns `v1` and `v2`, or `label` and `text`.

## 4. Run ETL and train
```bash
python -m src.etl
python -m src.train
```
Generated feature files and model artifacts are created locally and are ignored by Git.

## 5. Run tests
```bash
pytest -v
```

## 6. Run the Streamlit app
```bash
streamlit run app.py
```
Open http://localhost:8501.

## 7. MLflow
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```
Open http://127.0.0.1:5000. Run `python -m src.train` in another terminal to log runs.

## 8. Docker
```bash
docker build -t spam-streamlit:1.0 .
docker run --rm --name spam-container -p 8501:8501 spam-streamlit:1.0
```

## 9. Kubernetes (Docker Desktop Kubernetes)
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get deployments,pods,services
```
Open http://localhost:30085. The image must be available to the local cluster.

Cleanup:
```bash
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml
```

## 10. Terraform
The included Terraform configuration uses the Docker provider and expects the Docker daemon
to be running. From the project root:
```bash
cd terraform
terraform init
terraform validate
terraform plan
terraform apply
```
Destroy resources when finished:
```bash
terraform destroy
```

## 11. Prometheus and Grafana
The Streamlit process exposes Prometheus metrics on port 8000 at `/metrics`.
Start the app with the metrics server enabled (default) and run:
```bash
docker compose -f monitoring/docker-compose.yml up -d
```
Prometheus: http://localhost:9090
Grafana: http://localhost:3000 (admin / admin; change the password on first login).

## Notes
- Do not commit `.venv`, model binaries, MLflow databases, downloaded data, or secrets.
- The dataset is not bundled in this ZIP; download it using the script above.
- For GitHub, create an empty repository, then:
```bash
git init
git add .
git commit -m "chore: initialize SMS spam classifier MLOps project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/spam-classifier.git
git push -u origin main
```
