from retrieval import search
import sqlite3
import chromadb
from transformers import AutoModel, AutoTokenizer
import torch
import os
from create_embedding_base import EmbeddingModel
from retrieval import search
from creat_knowledge_base import creat_knowledge_base
import random
from collections import defaultdict
import config

data_path = "/work/home/acptye74du/log-rag-master/database/output.json"
base_path = config.SQLITE_DB_PATH
#  只需建立一次就好，不然会重复添加数据
base_table_name = 'test_1'
creat_knowledge_base(data_path,base_path,base_table_name)

db_path = os.path.join(base_path, "database.db")
# 连接 SQLite 数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
###############选取关系数据库对应的数据，最终选summary?#################
# cursor.execute("SELECT id, response, request_payload, response_code,level,attacktype,attackmeans, iswhiteip,eventtype FROM safe_1 LIMIT 20 OFFSET 1000")
cursor.execute("SELECT response, request_payload, response_code,level,attacktype FROM test_1")
#####################################################################
rows = cursor.fetchall()  # 获取查询结果,格式为元组的列表
conn.close()
test = []
test_label = []
for row in rows:
    # 假设 row 已经包含数据
    response, request_payload, response_code, level, attacktype = row  # 获取各个字段
    # 处理 None 值，避免报错
    response = response if response else ""
    request_payload = request_payload if request_payload else ""
    response_code = response_code if response_code else ""
    level = level if level else ""
    attacktype = attacktype if attacktype else ""
    # 创建字典保存 response、request_payload 和 response_code
    data_dict_1 = {
        "response": response,
        "request_payload": request_payload,
        "response_code": response_code
    }
    # 创建字典保存 level, attacktype, attackmeans, iswhiteip, eventtype
    data_dict_2 = {
        "level": level,
        "attacktype": attacktype
    }
    data_dict_1 = str(data_dict_1)
    # 将结果添加到 test 列表中
    test.append(data_dict_1)
    test_label.append(data_dict_2)

embedding_path = config.VECTOR_DB_PATH
model_path = config.EMBEDDING_MD_PATH
embedding_model = EmbeddingModel(model_path)

def analyze_label_accuracy(test, test_label, search, base_path, embedding_path, embedding_model, label_key="level"):
    """
    统计指定标签分类（如 attacktype 或 eventtype）的总数和正确分类数量，计算各类别的命中比例。

    参数：
    - test (list): 测试数据集（query文本）。
    - test_label (list): 对应的标签，每个是字典，包含 "attacktype" 或 "eventtype" 等字段。
    - search (function): 用于进行搜索的函数。
    - base_path (str): 基础路径，用于传递给 search 函数。
    - embedding_path (str): 嵌入模型路径，用于传递给 search 函数。
    - embedding_model (object): 嵌入模型对象，用于传递给 search 函数。
    - label_key (str): 需要统计的标签类别，如 "attacktype" 或 "eventtype"。
    """
    # 统计指定 label_key 命中情况
    label_stats = defaultdict(lambda: {"total": 0, "correct": 0})

    # 遍历测试数据集
    for index, query_text in enumerate(test):
        label = test_label[index]  # 真实标签
        label_value = label[label_key]  # 获取指定 label_key 的真实类别
        label_stats[label_value]["total"] += 1  # 该类别总数 +1

        # 获取模型预测结果
        results = search(query_text, base_path, embedding_path, embedding_model)

        # 只要有一个匹配的 label_key，就认为正确
        if any(label_value == result["label"][label_key] for result in results):
            label_stats[label_value]["correct"] += 1

    # 打印统计结果
    print(f"\n{label_key.capitalize()} 分类统计：")
    for label_value, stats in label_stats.items():
        total = stats["total"]
        correct = stats["correct"]
        accuracy = correct / total if total > 0 else 0
        print(f"{label_value}: 总数 {total}, 命中 {correct}, 命中率 {accuracy:.2f}")
analyze_label_accuracy(test, test_label, search, base_path, embedding_path, embedding_model, label_key="level")
