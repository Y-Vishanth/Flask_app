# Simple Flask App with Docker and GitHub Actions

A simple Flask REST API with health check endpoint, containerized with Docker and automatically built and deployed to EC2 using GitHub Actions CI/CD.

---

## 📁 Project Structure

```
my-flask-app/
├── app/
│   └── main.py                        ← Flask application
├── .github/
│   └── workflows/
│       └── ci-cd.yml                  ← GitHub Actions workflow
├── Dockerfile                         ← Docker configuration
├── .dockerignore                      ← Files to exclude from Docker
└── requirements.txt                   ← Python dependencies
```

---

## 🐍 Step 1: Python & Flask Setup on Ubuntu EC2

### 1.1 Connect to your EC2
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### 1.2 Update system & install Python
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv -y

# Verify installation
python3 --version
```

### 1.3 Create project folder
```bash
mkdir my-flask-app
cd my-flask-app
```

### 1.4 Create & activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
# You will see (venv) at the start of your terminal ✅
```

> ⚠️ **Important:** Run `source venv/bin/activate` every time you open a new terminal session.

### 1.5 Install Flask & generate requirements.txt
```bash
pip install flask
pip freeze > requirements.txt
```

### 1.6 Create the Flask app

Refer to `app/main.py` for the complete Flask application code.

The app exposes these routes:

| Route | Description |
|-------|-------------|
| `/` | Returns `Hello from Flask! 🚀` |
| `/health` | Returns `OK` — used for health checks |
| `/test` | Returns `It looks cool!` |

### 1.7 Run the Flask app
```bash
python3 app/main.py
```

### 1.8 Open port 5000 on EC2
1. Go to **AWS Console → EC2 → Security Groups**
2. Click **Edit Inbound Rules → Add Rule**
3. Set: Type = **Custom TCP**, Port = **5000**, Source = **0.0.0.0/0**
4. Save

### 1.9 Test the app

| URL | Expected Response |
|-----|------------------|
| `http://your-ec2-ip:5000/` | Hello from Flask! 🚀 |
| `http://your-ec2-ip:5000/health` | OK ✅ |
| `http://your-ec2-ip:5000/test` | It looks cool! |

---

## 🐳 Step 2: Docker Setup

### 2.1 Install Docker on Ubuntu EC2
```bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

# Allow ubuntu user to run docker without sudo
sudo usermod -aG docker ubuntu

# IMPORTANT: Logout and login again
exit
```

Log back in and verify:
```bash
docker --version
```

### 2.2 Dockerfile

Refer to `Dockerfile` for the complete Docker configuration.

### 2.3 Create .dockerignore file
```bash
nano .dockerignore
```

Add the following:
```
venv/
__pycache__/
*.pyc
*.pyo
.env
```

| Entry | Why ignored |
|-------|-------------|
| `venv/` | Not needed — Docker installs its own packages |
| `__pycache__/` | Python auto-generated cache files |
| `*.pyc` | Compiled Python files |
| `.env` | Secret keys — never send these! |

### 2.4 Build Docker image
```bash
cd ~/my-flask-app
docker build -t flask-app .
```

### 2.5 Run the container
```bash
docker run -d -p 5000:5000 --name flask-app flask-app
```

### 2.6 Verify container is running
```bash
docker ps
docker logs flask-app
```

### Useful Docker Commands
```bash
docker ps                    # List running containers
docker ps -a                 # List all containers (including stopped)
docker stop flask-app        # Stop container
docker start flask-app       # Start container
docker rm flask-app          # Remove container
docker rmi flask-app         # Remove image
docker logs flask-app        # View container logs
```

---

## ⚙️ Step 3: GitHub Actions CI/CD

The pipeline has **2 jobs** — build and deploy.

Refer to `.github/workflows/ci-cd.yml` for the complete workflow configuration.

### What the pipeline does:

**Job 1 — Build and Push:**
- Checks out the code
- Logs in to Docker Hub
- Builds the Docker image
- Pushes image to Docker Hub as `your-username/flask-app:latest`

**Job 2 — Deploy to EC2:**
- SSHs into your EC2 server
- Pulls the latest Docker image from Docker Hub
- Stops and removes the old container
- Runs the new container on port 5000

### 3.1 Required GitHub Secrets

Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions`

Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub access token (Read & Write) |
| `EC2_PUBLIC_IP` | Your EC2 public IP address |
| `EC2_USERNAME` | `ubuntu` |
| `EC2_SSH_KEY` | Your EC2 private key (contents of `.pem` file) |

### 3.2 Generate Docker Hub Access Token
1. Go to `https://hub.docker.com/settings/security`
2. Click **New Access Token**
3. Set permission to **Read & Write**
4. Copy the token ⚠️ shown only once!

### 3.3 Generate GitHub Personal Access Token (PAT)
1. Go to `https://github.com/settings/tokens`
2. Click **Generate new token (classic)**
3. Enable: ✅ `repo` and ✅ `workflow` scopes
4. Copy the token and use it as your GitHub password when pushing

### 3.4 Push code and trigger pipeline
```bash
git add .
git commit -m "Initial commit"
git branch -m master main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push origin main
```

Go to your GitHub repo → **Actions** tab to see the pipeline running! ✅

---

## 🔑 Common Issues & Fixes

| Error | Fix |
|-------|-----|
| `No module named flask` | Run `source venv/bin/activate` first |
| `venv/bin/activate: No such file` | Run `python3 -m venv venv` to create venv |
| `Permission denied` on docker | Run `sudo usermod -aG docker ubuntu` then logout/login |
| `index.lock: Permission denied` | Run `sudo chown -R ubuntu:ubuntu .git` |
| `src refspec main does not match` | Run `git branch -m master main` |
| `insufficient scopes` on Docker Hub | Regenerate token with Read & Write permission |
| `workflow scope` error on GitHub push | Regenerate PAT with `workflow` scope enabled |

---

## 📝 Quick Reference

```bash
# Activate venv
source venv/bin/activate

# Run Flask app locally
python3 app/main.py

# Build & run Docker locally
docker build -t flask-app .
docker run -d -p 5000:5000 --name flask-app flask-app

# Push to GitHub (triggers CI/CD automatically)
git add .
git commit -m "your message"
git push origin main
```

---

*Built with Python 🐍 | Flask 🌶️ | Docker 🐳 | GitHub Actions ⚙️*
