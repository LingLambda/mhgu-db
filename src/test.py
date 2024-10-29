
import json
import sqlite3
from bs4 import BeautifulSoup


info_list = []

monster_url = '../data/2992.html'
with open(monster_url, 'r', encoding='utf-8') as file:
    html = file.read()
soup = BeautifulSoup(html, 'html.parser')

# 假设 soup 是一个全局变量
element_soup = soup  # 在全局范围内定义 soup


def get_text_from_selector(selector):
    """从指定选择器获取文本."""
    element = element_soup.select_one(selector)
    return element.get_text(strip=True) if element else ''


def get_table_as_str(selector):
    """从指定选择器提取表格并转换为字符串."""
    table = element_soup.select_one(selector)
    return str(table) if table else ''


monster_info = {
    'monster_name': get_text_from_selector(
        '#main_1 > div > div.f_min > div:nth-child(2) > table > tbody'
    ),
    'monster_species': get_text_from_selector(
        '#main_1 > div > div.f_min > div:nth-child(2) > table > tbody > tr:nth-child(2) > td'
    ),
    'note': get_text_from_selector('#main_1 > div > div.f_min > div.box2'),
    'hitzone_table': get_table_as_str('#main_1 > div > div.f_min > div:nth-child(9) > div.col-sm-9 > table'),
    'de_state_table': get_table_as_str('#main_1 > div > div.f_min > div:nth-child(12) > div:nth-child(1) > table'),
    'item_well_table': get_table_as_str('#main_1 > div > div.f_min > div:nth-child(12) > div:nth-child(2) > table'),
    'from_table': get_table_as_str('#main_1 > div > div.f_min > table:nth-child(16)'),
}

# print(monster_info)


a = element_soup.select_one('#main_1 > div > div.f_min > div:nth-child(13) > div:nth-child(1) > table')
print(a)