import json
import os
import sqlite3
from bs4 import BeautifulSoup

# 连接 SQLite 数据库（如果不存在会自动创建）
db = sqlite3.connect('../db/mhgu.db')
cursor = db.cursor()


cursor.execute('''
select distinct Equip.url
from Equip
''')
#
rows = cursor.fetchall()

for row in rows:
    url = row[0]
    with open(url, 'r', encoding='utf-8') as file:
        html = file.read()
    element_soup = BeautifulSoup(html, 'html.parser')

    def get_text(selector):
        """从指定选择器获取文本."""
        element = element_soup.select_one(selector)
        return element.get_text(strip=True) if element else ''

    def get_html(selector):
        element = element_soup.select_one(selector)
        return str(element) if element else ''

    name =get_text('#main_1 > div > div.row_x > div > div.f_min > h3:nth-child(1)')
    html_div =get_html('.f_min')
    # print(html_div)
    soup = BeautifulSoup(html_div, 'html.parser')

    # 找到所有的 a 标签并进行替换
    for a in soup.find_all('a'):
        # 获取链接文本
        link_text = a.get_text(strip=True)
        # 创建新的 span 标签
        new_span = soup.new_tag('span', **{'class': 'c_g'})
        new_span.string = link_text
        # 替换 a 标签
        a.replace_with(new_span)


    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>装备信息表</title>
        <style>
        body {{
          font-family: 'Arial', sans-serif;
          background-color: #f5f5f5;
          margin: 0;
          padding: 20px;
        }}
        
        h3 {{
          text-align: center;
          color: #333;
        }}
        
        p {{
          text-align: center;
          font-style: italic;
          color: #666;
        }}
        
        .box1 {{
          margin: 10px auto;
          padding: 10px;
          max-width: 800px;
          background-color: #fff;
          border-radius: 8px;
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        
        .box1 span.c_r {{
          color: red;
          font-weight: bold;
        }}
        
        table.t1 {{
          width: 100%;
          margin: 20px 0;
          border-collapse: collapse;
          background-color: #fff;
          border-radius: 8px;
          overflow: hidden;
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        
        th, td {{
          border: 1px solid #ddd;
          padding: 12px;
          text-align: center;
        }}
        
        th {{
          background-color: #f8f8f8;
          color: #333;
          font-weight: bold;
        }}
        
        .progress {{
          background-color: #e0e0e0;
          border-radius: 4px;
          overflow: hidden;
        }}
        
        .progress-bar {{
          background-color: #76c7c0;
          color: white;
          text-align: center;
        }}
        
        tr:nth-child(even) {{
          background-color: #f9f9f9;
        }}
        
        a {{
          color: #337ab7;
          text-decoration: none;
        }}
        
        a:hover {{
          text-decoration: underline;
        }}

        </style>
    </head>
    <body>
        {soup}
    </body>
    </html>
    """
    # 创建 BeautifulSoup 对象
    soup = BeautifulSoup(html_content, 'html.parser')

    # 处理所有 img 标签
    for img in soup.find_all('img'):
        alt_text = img.get('alt')  # 获取 alt 属性的值
        if alt_text:  # 如果 alt 属性存在
            img.insert_before(alt_text)  # 插入 alt 文本
        img.decompose()  # 删除 img 标签

    # 获取处理后的 HTML
    cleaned_html = str(soup)


    name =  name.replace('/', '_')
    file_path = '..\\ouput_html2\\'+name +'.html'
    directory = os.path.dirname(file_path)

    # 创建目录（如果它不存在的话）
    if not os.path.exists(directory):
        os.makedirs(directory)
    # 写入 HTML 内容到文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_html)

