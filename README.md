# DevOps 监控管理平台 (DevOps Monitoring Platform)

基于 Docker Compose 构建的一套完整的服务器监控与管理系统。采用 Nginx 负载均衡、Flask 后端、Redis 缓存、MySQL 持久化，并集成了 Prometheus + Grafana 的全链路监控。

## 🏗️ 系统架构

```text
      用户浏览器
          │
          ▼
   [Nginx 负载均衡器 (lb)] (端口: 8080)
          │
    ┌─────┴─────┐
    ▼           ▼
[Flask web1] [Flask web2] (提供管理后台页面)
    │           │
    ├───────────┴───────────┐
    ▼                       ▼
[Redis] (缓存访问计数)   [MySQL] (存储用户/告警/日志数据)
                            │
                            ▼
                     [Prometheus] (监控数据采集)
                            │
                            ▼
                     [Node Exporter] (暴露宿主机指标)
                            │
                            ▼
                       [Grafana] (可视化图表)
🛠️ 技术栈
容器化与编排：Docker / Docker Compose

Web 服务器与代理：Nginx (反向代理、负载均衡)

后端应用：Python 3.9 / Flask / Flask-Login

数据库与缓存：MySQL 8.0 / Redis (Alpine)

监控与可视化：Prometheus / Node Exporter / Grafana

操作系统：CentOS 7 (虚拟机环境)

📦 核心功能
高可用负载均衡：Nginx 将前端请求轮询分发至两个 Flask 后端（web1/web2），支持单节点故障容错。

动态监控大盘：管理后台实时查询 Prometheus API，展示服务器的 CPU、内存、磁盘和系统负载。

用户登录认证：基于 Flask-Login 和 MySQL，实现安全的用户鉴权与 Session 管理。

数据持久化与缓存：MySQL 持久化存储业务数据，Redis 缓存热点访问计数。

全链路监控：Node Exporter 采集宿主机硬件指标，Prometheus 负责存储与告警规则计算，Grafana 负责高级可视化。

🚀 快速启动
1. 前置要求
已安装 Docker 与 Docker Compose

宿主机已放行相关端口（8080, 9090, 3000）

2. 启动项目
bash
# 克隆项目
git clone https://github.com/gabecole7935-crypto/devops-monitoring-platform.git
cd devops-monitoring-platform

# 构建并启动所有容器
docker compose up -d --build
3. 访问服务
服务	访问地址	默认账号
管理后台	http://localhost:8080	admin / admin123
Prometheus	http://localhost:9090	无
Grafana	http://localhost:3000	admin / admin
🛡️ 故障排查与验证记录
在开发部署过程中，我排除了以下典型故障：

502 Bad Gateway：发现 web1 容器处于 Restarting 状态。使用 docker logs web1 定位到 Python 代码缺失依赖，重新 build 后恢复。

宿主机无法访问 8080 端口：排查发现是 VMware NAT 模式未配置端口转发，且宿主机防火墙未放行端口。通过配置 NAT 端口映射和 firewall-cmd 解决。

Docker 拉取镜像超时：通过配置国内镜像加速器（daemon.json）和修改 DNS 解决。

Nginx 启动失败：修改 default.conf 后，使用 docker exec lb nginx -t 检查语法，定位到 proxy_pass 缺少 http:// 协议，修复后 reload 恢复。

📂 目录结构
text
.
├── docker-compose.yml          # 容器编排文件
├── prometheus.yml              # Prometheus 采集配置
├── lb/                         # Nginx 负载均衡配置
│   └── default.conf
├── web1/                       # 后端实例 1 (Flask)
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── templates/              # HTML 模板 (登录页、大盘)
└── web2/                       # 后端实例 2 (与 web1 相同，用于高可用)
