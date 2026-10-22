from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
import redis
import pymysql
import os
import requests

app = Flask(__name__)
app.secret_key = 'change-this-secret-key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

r = redis.Redis(host='redis', port=6379, decode_responses=True)
PROM = 'http://prometheus:9090/api/v1/query'

def get_db():
    return pymysql.connect(
        host='mysql', user='root', password='123456',
        database='testdb', cursorclass=pymysql.cursors.DictCursor
    )

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    u = cursor.fetchone()
    conn.close()
    if u:
        return User(u['id'], u['username'], u['role'])
    return None

def query_prom(expr):
    try:
        resp = requests.get(PROM, params={'query': expr}, timeout=3)
        result = resp.json()['data']['result']
        if result:
            return round(float(result[0]['value'][1]), 1)
    except Exception:
        pass
    return 'N/A'

def log_action(action):
    conn = get_db()
    cursor = conn.cursor()
    username = current_user.username if current_user.is_authenticated else 'anonymous'
    cursor.execute("INSERT INTO audit_logs (username, action) VALUES (%s, %s)", (username, action))
    conn.commit()
    conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        u = cursor.fetchone()
        conn.close()
        if u and check_password_hash(u['password'], password):
            user = User(u['id'], u['username'], u['role'])
            login_user(user)
            log_action(f"用户 {username} 登录成功")
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    log_action(f"用户 {current_user.username} 退出")
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    cpu = query_prom('100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)')
    mem = query_prom('(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100')
    disk = query_prom('(1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100)')
    load = query_prom('node_load1')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS c FROM servers")
    server_count = cursor.fetchone()['c']
    cursor.execute("SELECT COUNT(*) AS c FROM alerts WHERE status='firing'")
    alert_count = cursor.fetchone()['c']
    conn.close()

    return render_template('dashboard.html', cpu=cpu, mem=mem, disk=disk, load=load, server_count=server_count, alert_count=alert_count)

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)