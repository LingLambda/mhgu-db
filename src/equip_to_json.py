import json
import os

def scan_directory(directory):
    file_names = []
    # 遍历目录下的所有文件和子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):  # 检查文件是否以 .html 结尾
                file_names.append(file[:-5])  # 去掉 .html 后缀并添加到列表中
    return file_names

# 使用示例
directory_path = '../ouput_html2'
file_list = scan_directory(directory_path)
# 将文件名列表转换为 JSON 并写入文件
json_file_path = './equip_index.json'  # JSON 文件保存路径
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(file_list, json_file, ensure_ascii=False)  # 写入 JSON 数据