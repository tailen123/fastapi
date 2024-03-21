import json
from http.client import HTTPException
from fastapi import FastAPI, Depends, HTTPException, status

import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    # 端口号
    port=3306,
    # 用户名
    user='root',
    # 密码
    passwd='12345678',
    # 数据库名称
    db='order_database',
    # 字符编码格式
    charset='utf8mb4')

cur = conn.cursor()

jsonPath = '/Users/qingdu/Desktop/pythonpj/pythonProject/ManageOrder/database/all.json'
with open(jsonPath, 'r', encoding='utf_8_sig') as file:
    # 解析为字典型
    all_data = json.load(file)
    result_data = all_data["results"]
    for message in result_data:
        key_values = ', '.join('`{}` = %s'.format(k) for k in message.keys())
        values = tuple(message.values())
        cur.execute("INSERT INTO result_table SET " + key_values, values)
        conn.commit()

cur.close()
conn.close()
