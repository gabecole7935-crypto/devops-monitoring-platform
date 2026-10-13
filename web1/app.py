from flask import Flask
import redis
import pymysql
import os

app = Flask(__name__)

r = redis.Redis(host='redis', port=6379, decode_responses=True)

def get_db():
    return pymysql.connect(
        host='mysql',
        user='root',
        password='123456',
        database='testdb'
    )

@app.route('/')
def index():
    count = r.get('visit_count')
    if count is None:
        count = 0
    count = int(count) + 1
    r.set('visit_count', count)
    hostname = os.environ.get('HOSTNAME', 'unknown')
    return f"<h1>Backend {hostname}</h1><p>访问次数：{count}</p>"

@app.route('/db')
def db_test():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 'MySQL connected' AS msg")
    result = cursor.fetchone()
    conn.close()
    return f"<h1>{result[0]}</h1>"

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
