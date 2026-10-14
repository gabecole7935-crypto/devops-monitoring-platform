@app.route('/')
def index():
    # Redis：访问计数
    count = r.get('visit_count')
    if count is None:
        count = 0
    count = int(count) + 1
    r.set('visit_count', count)

    # MySQL：查当前时间
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT NOW()")
    db_time = cursor.fetchone()[0]
    conn.close()

    hostname = os.environ.get('HOSTNAME', 'unknown')

    # 读取简历 HTML
    with open('/app/templates/resume.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 顶部横幅
    banner = f'''
    <div style="background:#0071e3;color:white;text-align:center;padding:10px;font-size:14px;">
        Backend: {hostname} | Redis访问次数: {count} | MySQL时间: {db_time}
    </div>
    '''
    return banner + html
