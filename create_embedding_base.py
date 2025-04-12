import chromadb
from transformers import AutoModel, AutoTokenizer
import sqlite3
import torch
import os
import config


class EmbeddingModel:
    def __init__(self, model_path):
        """初始化模型和分词器"""
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModel.from_pretrained(model_path)

    def get_embedding(self, text):
        """计算文本嵌入"""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy().tolist()
        return embeddings

def create_embedding_base(embedding_table_name,base_path,embedding_path,embedding_model):
    """
        创建向量知识库，并将相关数据从关系数据库导入到关系数据库中，唯一id一一对应。
        参数:
        embedding_table_name (str): 向量数据表的名称，数据将被导入到该表中。
        base_path (str): SQLite 数据库的路径，用于存储关系数据。
        embedding_path (str): 数据库的路径，用于存储向量数据。
    """

    # 连接 SQLite获取对应的数据
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    db_path = os.path.join(base_path, "database.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    ###############选取关系数据库对应的数据，最终选summary#################
    cursor.execute("SELECT id, response, request_payload,response_code FROM safe_1 ")
    rows = cursor.fetchall()  # 获取查询结果,格式为元组的列表
    # 连接 ChromaDB
    client = chromadb.PersistentClient(path=embedding_path)  # 持久化存储
    collection = client.create_collection(
    name= embedding_table_name,
    metadata={"hnsw:space": "cosine"}  # l2 is the default
)
    # 处理并存入 ChromaDB
    count = 0
    for row in rows:
        doc_id, response, request_payload,response_code = row  # 获取 id、response 和 request_payload
        # 处理 None 值，避免报错
        response = response if response else ""
        request_payload = request_payload if request_payload else ""
        response_code = response_code if response_code else ""
        data_dict = {
                    "response": response,
                    "request_payload": request_payload,
                    "response_code": response_code
                    }
        # 合并 response 和 request_payload 为 text
        text = str(data_dict)
        text_embedding = embedding_model.get_embedding(text)
        # 将合并后的文本存入 ChromaDB
        collection.add(
            ids=[doc_id],  # 唯一 ID
            embeddings=[text_embedding],
            metadatas=[{"type": "text"}]  # 存储 "type" 字段
        )
        count += 1
        if count % 10 == 0:
            print(f"已存入第 {count} 条数据")
    # 关闭 SQLite 连接
    conn.close()
    print(" 数据已成功存入 ChromaDB！")
#######################################
# # 储存向量数据
# # 加载嵌入模型
# model_path = config.EMBEDDING_MD_PATH
# embedding_model = EmbeddingModel(model_path)
# embedding_table_name = "embedding_table"
# base_path = config.SQLITE_DB_PATH
# embedding_path = config.VECTOR_DB_PATH
# create_embedding_base(embedding_table_name,base_path,embedding_path,embedding_model)

################################################
# #检查存储结果
# client = chromadb.PersistentClient(path=embedding_path)  # 这里使用本地文件存储数据库
# print("已经储存的向量表")
# print(client.list_collections())
# # 查询集合中的数据总条数
# collection = client.get_collection(name="embedding_table")
# num_records = collection.count()
# print(f"ChromaDB 存储的总数据量: {num_records}")
# # 获取前 3 条数据
# results = collection.get(limit=3, include=["metadatas", "embeddings", "documents"])
#
# # 打印 ID、元数据（metadata）、嵌入向量（embeddings）
# for i, doc_id in enumerate(results["ids"]):
#     print(f"\n 数据条目 {i+1}:")
#     print(f" ID: {doc_id}")
#     print(f"Metadata: {results['metadatas'][i]}")
#     print(f" Document: {results['documents'][i] if 'documents' in results else '无文档'}")
#     print(f"Embedding (向量) 维度: {len(results['embeddings'][i])}")