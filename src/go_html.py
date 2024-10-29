import json
import os

# 指定 JSON 文件的路径
file_path = 'data.json'

# 打开 JSON 文件并读取内容
with (open(file_path, 'r', encoding='utf-8') as json_file):
    data = json.load(json_file)

    for i in data:
        de_state_table = (i['de_state_table']) if i['de_state_table'] else ''
        note = '备注:'+i['note'] if i['note'] else ''

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
            <h3>名称: {i['monster_name']} 种: {i['monster_species']}</h3>
            <p>{note}</p>
            {i['hitzone_table']}
            {de_state_table}
            {i['item_well_table']}
            {i['from_table']}
        </body>
        </html>

        """
        file_path = f'..\\ouput_html\\{i['monster_name']}.html'
        directory = os.path.dirname(file_path)

        # 创建目录（如果它不存在的话）
        if not os.path.exists(directory):
            os.makedirs(directory)
        # 写入 HTML 内容到文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
