import json
import sqlite3
from bs4 import BeautifulSoup

# 连接 SQLite 数据库（如果不存在会自动创建）
db = sqlite3.connect('../db/mhgu.db')
cursor = db.cursor()

# 创建表（如果不存在）
cursor.execute('''SELECT * FROM monster_url''')

rows = cursor.fetchall()

info_list = []

for row in rows:
    monster_url = row[2]
    with open(monster_url, 'r', encoding='utf-8') as file:
        html = file.read()
    element_soup = BeautifulSoup(html, 'html.parser')


    def get_text_from_selector(selector):
        """从指定选择器获取文本."""
        element = element_soup.select_one(selector)
        return element.get_text(strip=True) if element else ''


    def get_table_as_str(selector):
        """从指定选择器提取表格并转换为字符串."""
        table = element_soup.select_one(selector)
        return str(table) if table else ''


    monster_name = get_text_from_selector('#main_1 > div > div.f_min > div:nth-child(2) > table tr:nth-child(1) td.b')
    # monster_species = get_text_from_selector('#main_1 > div > div.f_min > div:nth-child(2) > table tr:nth-child(2) td.b')
    # from_table = get_table_as_str('#main_1 > div > div.f_min > table:nth-child(16)')
    # note = get_text_from_selector('#main_1 > div > div.f_min > div.box2')
    #
    # if monster_name != '阁螳螂' and monster_name != '阁螳螂·机甲':
    #     hizone_table = get_table_as_str('#main_1 > div > div.f_min > div:nth-child(8) > div.col-sm-9 > table')
    #     de_state_table = get_table_as_str('#main_1 > div > div.f_min > div:nth-child(12) > div:nth-child(1) > table')
    #     item_well_table = get_table_as_str('#main_1 > div > div.f_min > div:nth-child(12) > div:nth-child(2) > table')
    # else:
    #     hizone_table = get_table_as_str('#main_1 > div > div.f_min > div:nth-child(9) > div.col-sm-9 > table')
    #     de_state_table = get_table_as_str('#main_1 > div > div.f_min > div:nth-child(13) > div:nth-child(1) > table')
    #     item_well_table = get_table_as_str('#main_1 > div > div.f_min > div:nth-child(13) > div:nth-child(2) > table')

    # monster_info = {
    #     'monster_name': monster_name,
        # 'monster_species': monster_species,
        # 'note': note,
        # 'hitzone_table': hizone_table,
        # 'de_state_table': de_state_table,
        # 'item_well_table': item_well_table,
        # 'from_table': from_table,
    # }

    # 现在 monster_info 对象中包含了所有需要的数据

    # print(monster_info)
    info_list.append(monster_name)

with open('monster_index.json', 'w', encoding='utf-8') as json_file:
    json.dump(info_list, json_file, ensure_ascii=False)
