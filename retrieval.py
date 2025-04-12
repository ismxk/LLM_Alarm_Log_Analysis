import sqlite3
import chromadb
from transformers import AutoModel, AutoTokenizer
import torch
import os
import config
from create_embedding_base import EmbeddingModel
# 连接数据库
def search(query_text,base_path,embedding_path,embedding_model):
    """
        对于输入的文本，检索出对应的相似数据。
        参数:
        query_text (str): 输入用于检索的文本。
        base_path (str): SQLite 数据库的路径，用于存储关系数据。
        embedding_path (str): 数据库的路径，用于存储向量数据。
        返回：
        每条检索结果为字典，所有结果存为列表
    """
    db_path = os.path.join(base_path, "database.db")
    # 连接 SQLite 数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # 连接 ChromaDB
    client = chromadb.PersistentClient(path=embedding_path)  # 持久化存储
    collection = client.get_collection(name="embedding_table")
    query_text = embedding_model.get_embedding(query_text)
    # 执行向量检索
    results = collection.query(
        query_embeddings=[query_text],
        n_results=3  # 返回最近 3 个
    )
    # 获取最相似文档的 ID
    similar_doc_ids = [int(i) for i in results["ids"][0]]  # 转换回整数
    similarities = results["distances"][0]  # 获取对应的相似度
    # 👉 在 SQLite 数据库中查询完整信息（仅选择部分字段，如 id, response, request_payload）
    cursor.execute(
        f"SELECT id, response, request_payload,response_code, level, attacktype FROM safe_1 WHERE id IN ({','.join(['?'] * len(similar_doc_ids))})",
        similar_doc_ids
    )
    matched_rows = cursor.fetchall()
    # 关闭数据库连接
    conn.close()
    # 👉 结合 SQLite 查询结果和相似度，并只输出部分字段
    results = []
    for idx, row in enumerate(matched_rows):
        result = {}
        doc_id, response, request_payload, response_code, level, attacktype = row
        similarity = similarities[idx]  # 获取对应的相似度
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
        # data_dict_1 = str(data_dict_1)
        # data_dict_2 = str(data_dict_2)
        # result["id"] = doc_id
        # result["similarity"] = similarity
        result["text"] = data_dict_1
        result["label"] =data_dict_2
        results.append(result)
    return results

    # # test
# if __name__ == '__main__':
#     model_path = config.EMBEDDING_MD_PATH
#     embedding_model = EmbeddingModel(model_path)
#     base_path = config.SQLITE_DB_PATH
#     embedding_path = config.VECTOR_DB_PATH
#     query_text =''' "response":"HTTP/1.1 200 OK\r\nAccept-Ranges: bytes\r\nCache-Control: public,max-age=86400\r\nContent-Disposition: attachment\r\nContent-Length:
#     3145\r\nContent-Security-Policy: default-src 'none'\r\nContent-Type: application/x-chrome-extension\r\nEtag: \"2dbb5f4\"\r\nServer: downloads\r\nX-Content-Type-Options
#     : nosniff\r\nX-Frame-Options: SAMEORIGIN\r\nX-Xss-Protection: 0\r\nDate: Wed, 05 Feb 2025 21:41:57 GMT\r\nAlt-Svc: h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000
#     \r\nLast-Modified: Wed, 17 Jul 2024 20:43:45 GMT\r\nConnection: keep-alive\r\nVary: Origin\r\n\r\n","domain":" r4---sn-ni5eln7e.gvt1-cn.com","request_payload":
#     "|||||HEAD /edgedl/chromewebstore/L2Nocm9tZV9leHRlbnNpb24vYmxvYnMvYjhkYWYwZDctOTExOS00MGQ5LTgyNjAtN2FlY2ZjMDg0NmNj/1.0.0.17_llkgjffcdpffmhiakmfcdcblohccpfmo
#     .crx?cms_redirect=yes&met=1738843314,&mh=yB&mip=39.173.116.133&mm=28&mn=sn-ni5eln7e&ms=nvh&mt=1738842973&mv=m&mvi=4&pl=22&rmhost=r3---sn-ni5eln7e.gvt1-cn.
#     com&rms=nvh,nvh&shardbypass=sd&smhost=r4---sn-ni5eln7z.gvt1-cn.com HTTP/1.1\r\nConnection: Keep-Alive\r\nAccept: */*\r\nAccept-Encoding: identity\r\nUser-
#     Agent: Microsoft BITS/7.8\r\nHost: r4---sn-ni5eln7e.gvt1-cn.com\r\n\r\n" '''
#     a = search(query_text,base_path,embedding_path,embedding_model)
#     print(len(a))
#     print(a[0])
#     # 输出结果
#     b= a[0]["label"]
#     print(b)
#     print(b["level"])


