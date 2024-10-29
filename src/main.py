import sqlite3
from bs4 import BeautifulSoup

# 连接 SQLite 数据库（如果不存在会自动创建）
db = sqlite3.connect('../db/mhgu.db')
cursor = db.cursor()

# 创建表（如果不存在）
cursor.execute("""
    CREATE TABLE IF NOT EXISTS monster_url (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        url TEXT
    )
""")

with open('../2501.html', 'r', encoding='utf-8') as file:
    html = file.read()

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(html, 'html.parser')
navi_div = soup.find('div', id='navi1')  # 找到 id 为 navi1 的 div

# 从 navi1 中提取所有 a 标签
links = navi_div.find_all('a')

# 提取数据并插入到 SQLite 数据库
for link in links:
    text = link.get_text().strip()  # 获取 a 标签的文本
    url = link.get('href')  # 获取 a 标签的 href 属性
    cursor.execute("INSERT INTO monster_url (text, url) VALUES (?, ?)", (text, url))

# 提交更改并关闭数据库连接
db.commit()
cursor.close()
db.close()

print("done!")
