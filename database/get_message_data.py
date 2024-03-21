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

# createTableSql = (
#     'CREATE TABLE IF NOT EXISTS message_table('
#     'id INT PRIMARY KEY AUTO_INCREMENT,'
#     'dialog_id INT,'
#     'text VARCHAR(50),'
#     'text_zh VARCHAR(50),'
#     'created_at VARCHAR(50),'
#     'stage INT,'
#     'from_user BOOLEAN,'
#     'reason VARCHAR(50),'
#     'reason_type VARCHAR(50),'
#     'is_del BOOLEAN,'
#     'message_id INT) '
#     'ENGINE=InnoDB DEFAULT CHARSET=utf8;'
# )
# try:
#     cur.execute(createTableSql)
# except pymysql.Error as e:
#     error = f"str{e}"
#     raise HTTPException(status_code=401, detail=error)

jsonPath = '/Users/qingdu/Desktop/pythonpj/pythonProject/ManageOrder/database/all.json'
with open(jsonPath, 'r', encoding='utf_8_sig') as file:
    #解析为字典型
    all_data = json.load(file)
    data = all_data["messages"]
    for message in data:
        key_values = ', '.join('`{}` = %s'.format(k) for k in message.keys())
        values = tuple(message.values())
        cur.execute("INSERT INTO message_table SET " + key_values, values)
        conn.commit()


cur.close()
conn.close()

# file_data = file.read()
# data = json.loads(file_data)
#     for message in data:
#         id = message.get('id')
#         dialog_id = message['dialog_id']
#         text = message['text']
#         text_zh = message['text_zh']
#         created_at = message['created_at']
#         stage = message['stage']
#         from_user = message['from_user']
#         reason = message['reason']
#         reason_type = message['reason_type']
#         is_del = message['is_del']
#         message_id = message['message_id']
#
#         table = 'message_table'
#         insert_query = "INSERT INTO message_table (id, dialog_id, text,text_zh,created_at,stage,from_user,reason,reason_type,is_del,message_id) VALUES (%d, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"
#
#         cur.execute(insert_query, (
#             id, dialog_id, text, text_zh, created_at, stage, from_user, reason, reason_type, is_del, message_id))
#
# conn.commit()
# cur.close()
# conn.close()
