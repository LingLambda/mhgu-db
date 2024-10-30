# import json
# import os
#
# # 指定 JSON 文件的路径
# file_path = 'data.json'
#
# # 打开 JSON 文件并读取内容
# with (open(file_path, 'r', encoding='utf-8') as json_file):
#     data = json.load(json_file)
#
#     for i in data:
#         de_state_table = (i['de_state_table']) if i['de_state_table'] else ''
#         note = '备注:'+i['note'] if i['note'] else ''
#
#         html_content = f"""
#         <!DOCTYPE html>
#         <html lang="zh">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>怪物信息表</title>
#
#         </head>
#         <body>
#             <h3>名称: {i['monster_name']} 种: {i['monster_species']}</h3>
#             <p>{note}</p>
#             {i['hitzone_table']}
#             {de_state_table}
#             {i['item_well_table']}
#             {i['from_table']}
#         </body>
#         </html>
#
#         """
#         file_path = f'..\\ouput_html\\{i['monster_name']}.html'
#         directory = os.path.dirname(file_path)
#
#         # 创建目录（如果它不存在的话）
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#         # 写入 HTML 内容到文件
#         with open(file_path, 'w', encoding='utf-8') as file:
#             file.write(html_content)

import json
import os
import sqlite3
from bs4 import BeautifulSoup,NavigableString
# 连接 SQLite 数据库（如果不存在会自动创建）
db = sqlite3.connect('../db/mhgu.db')
cursor = db.cursor()

cursor.execute('''
select distinct *
from monster_url
''')
#
rows = cursor.fetchall()
count = 0;
for row in rows:
    count=count+1
    print(f'''处理第{count}个,总{len(rows)}个''')
    name = row[1]
    url = row[2]
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
    html_div = get_html('.f_min')
    # print(html_div)
    soup = BeautifulSoup(html_div, 'html.parser')

    target_div1 = soup.select_one('.f_min > div:nth-child(2)')
    target_div2 = soup.select_one('.f_min > div:nth-child(3)')
    if target_div1:
        target_div1.decompose()  # 删除该元素
    if target_div2:
        target_div2.decompose()  # 删除该元素

    # 找到所有的 a 标签并进行替换
    for a in soup.find_all('a'):
        # 获取链接文本
        link_text = a.get_text(strip=True)
        # 创建新的 span 标签
        new_span = soup.new_tag('span', **{'class': 'c_g'})
        new_span.string = link_text
        # 替换 a 标签
        a.replace_with(new_span)


    def replace_in_soup(soup, old_string, new_string):
        # 遍历所有的标签
        for element in soup.find_all(string=True):  # 获取所有文本节点
            if isinstance(element, NavigableString):  # 确保是文本节点
                element.replace_with(element.replace(old_string, new_string))  # 替换

    replace_in_soup(soup,'效色やすさ','触发容易度')
    replace_in_soup(soup,'乗り','骑乘')
    replace_in_soup(soup,'时間','时间')
    replace_in_soup(soup,'イベ上','上位活动')
    replace_in_soup(soup,'イベG','G位活动')
    replace_in_soup(soup,'チャレ','挑战任务')
    replace_in_soup(soup,'怒り','发怒')
    replace_in_soup(soup,'アトラルカ的形态変化后は','变化后的形态参见')
    replace_in_soup(soup,'アトラル王座','阁螳螂·机甲')
    replace_in_soup(soup,'アトラル王座的形态変化前は','变化前的形态参见')
    replace_in_soup(soup,'耐久値が0に之る与、ひるみや部位破坏が发生。下段は切断耐久値',
                    '耐久值归零会触发硬直和部位破坏,下方为切断的耐久值')
    replace_in_soup(soup,' 耐久値的狞猛化欄は狞猛化时的耐久値。下段はオーラ发生时',
                    '在“狞猛化”状态下耐久值有特定的表现,下方为发生效果时的表现')
    replace_in_soup(soup,'アトラルカ','阁螳螂')
    replace_in_soup(soup,'へ','')
    replace_in_soup(soup,'ダメージ','伤害')
    replace_in_soup(soup,'雪だるま','雪人')
    replace_in_soup(soup,'糸だるま','线达摩')
    replace_in_soup(soup,'个体剥ぎ取り','剥取个体')
    replace_in_soup(soup,'落与し物','掉落物')
    replace_in_soup(soup,'フリー狩猎','自由狩猎')
    replace_in_soup(soup,'[左ほど有效]','[越往左越有效]')
    replace_in_soup(soup,'ゲージ中央は各怪物的平均値','量规中央是各怪物的平均值')
    replace_in_soup(soup,'毒伤害は时间経過时的総伤害','毒伤害是经过总时间的伤害')
    replace_in_soup(soup,'二つ名怪物から入手で色る素材は任务LVによって変わります。'
                    ,'二名怪物得到的颜色素材根据任务LV不同而变化。')

    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>怪物信息表</title>
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
    padding: 15px; 
    background-color: #f9f9f9; 
    border: 1px solid #ddd; 
    border-radius: 8px; 
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); 
}}

.box2 {{ 
    margin: 10px auto; 
    padding: 15px; 
    background-color: #f9f9f9; 
    border: 1px solid #ddd; 
    border-radius: 8px; 
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); 
}}

.box1 span.c_r {{ 
    color: red; 
    font-weight: bold; 
}}

.table-container {{ 
    width: 100%; 
    margin: 20px 0; 
}}

table.t1 {{ 
    width: 100%; 
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

td {{ 
    background-color: #ffffff; 
}}

tr:nth-child(even) {{ 
    background-color: #f9f9f9; 
}}

.progress {{ 
    background-color: #e0e0e0; 
    border-radius: 5px; 
}}

.progress-bar {{ 
    background-color: #76c7c0; 
    color: white; 
    text-align: center; 
    height: 100%; 
    border-radius: 5px; 
}}

.c_g {{ 
    color: #5CB85C; 
}}

a {{ 
    color: #337ab7; 
    text-decoration: none; 
}}

a:hover {{ 
    text-decoration: underline; 
}}

.sp_only {{ 
    display: none; 
}}

@media (max-width: 768px) {{ 
    .sp_only {{ 
        display: inline; 
    }}

    .pc_only {{ 
        display: none; 
    }} 
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

    name = name.replace('/', '_')
    file_path = '..\\ouput_html3\\' + name + '.html'
    directory = os.path.dirname(file_path)

    # 创建目录（如果它不存在的话）
    if not os.path.exists(directory):
        os.makedirs(directory)
    # 写入 HTML 内容到文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_html)

