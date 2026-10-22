# 🚀 DevOps Monitoring Platform

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)](https://prometheus.io/)

**🌐 Language: [English](README.md) | [简体中文](README_zh.md)**

A high-availability server monitoring and management system built with Docker Compose. It integrates Nginx load balancing, Flask backend, Redis cache, MySQL persistence, and a full-link monitoring closed loop with Prometheus + Grafana.

## 🏗️ Architecture

```text
      Browser
         │
         ▼
 [Nginx Load Balancer (lb)] (Port: 8080)
         │
   ┌─────┴─────┐
   ▼           ▼
[Flask web1] [Flask web2] (Web Dashboard)
   │           │
   ├───────────┴───────────┐
   ▼                       ▼
[Redis] (Cache)         [MySQL] (Data Persistence)
                           │
                           ▼
                    [Prometheus] (Metrics Collection)
                           │
                           ▼
                    [Node Exporter] (Host Metrics)
                           │
                           ▼
                      [Grafana] (Visualization)
🛠️ Tech Stack
Containerization & Orchestration: Docker / Docker Compose

Web Server & Proxy: Nginx (Reverse Proxy, Load Balancing)

Backend: Python 3.9 / Flask / Flask-Login

Database & Cache: MySQL 8.0 / Redis (Alpine)

Monitoring & Visualization: Prometheus / Node Exporter / Grafana

OS: CentOS 7

✨ Key Features
High Availability: Nginx round-robin distributes requests to two Flask backends (web1/web2) for fault tolerance.

Dynamic Dashboard: The backend queries the Prometheus API in real-time to display CPU, memory, disk, and load averages.

Authentication: Secure user authentication and session management based on Flask-Login and MySQL.

Persistence & Caching: MySQL persists user and log data, while Redis caches hot access counts.

Full-link Observability: Node Exporter collects host metrics, Prometheus calculates alerting rules, and Grafana provides advanced visualization.

🚀 Quick Start
1. Prerequisites
Docker and Docker Compose installed

Ports (8080, 9090, 3000) allowed on the host firewall

2. Deployment
bash
# Clone the repository
git clone https://github.com/gabecole7935-crypto/devops-monitoring-platform.git
cd devops-monitoring-platform

# Build and start all containers in the background
docker compose up -d --build
3. Access Services
Service	URL	Default Credentials
Web Dashboard	http://localhost:8080	admin / admin123
Prometheus	http://localhost:9090	None
Grafana	http://localhost:3000	admin / admin
🛡️ Troubleshooting
During deployment, I resolved several typical issues:

502 Bad Gateway: Found web1 container in Restarting state. Used docker logs web1 to identify missing Python dependencies, rebuilt to fix.

Host Unreachable: Resolved NAT port forwarding issues in VMware and configured firewall-cmd on the host.

Docker Pull Timeout: Configured a domestic Docker registry mirror and DNS settings.

Nginx Start Failure: Used docker exec lb nginx -t to locate the missing http:// in proxy_pass, fixed and reloaded.

📂 Directory Structure
text
.
├── docker-compose.yml          # Orchestration file
├── prometheus.yml              # Prometheus config
├── lb/                         # Nginx load balancer config
│   └── default.conf
├── web1/                       # Backend Instance 1
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── templates/
└── web2/                       # Backend Instance 2 (same as web1)
