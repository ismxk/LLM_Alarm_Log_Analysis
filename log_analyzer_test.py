import string
import json
from model import generate_query_with_qwen, analyze_with_qwen, init_llm
from prompts import prompt2
import config
from retrieval import search
from create_embedding_base import EmbeddingModel
import re
# from rag import search_logs
# import storage

def analyze_log(log_entry, llm):
    """日志分析核心流程"""
    
    # 2️ 使用 Qwen 生成查询关键词
    # query_text = generate_query_with_qwen(llm, log_entry)
    # print("\n下面是大模型抽取关键词：\n")
    # print(query_text)
    # print("\n1 完毕\n")

    # 3️ RAG 检索相关日志
    model_path = config.EMBEDDING_MD_PATH
    embedding_model = EmbeddingModel(model_path)
    base_path = config.SQLITE_DB_PATH
    embedding_path = config.VECTOR_DB_PATH
    # retrieved_logs = search(query_text,base_path,embedding_path,embedding_model)
    retrieved_logs = search(log_entry,base_path,embedding_path,embedding_model)


    # 4️ 构建 Qwen 分析 Prompt
    formatted_prompt = prompt2.format(log_entry=log_entry, retrieved_logs=retrieved_logs)
    cleaned_logs = re.sub(r'[\?§©¨µè]{2,}', '', formatted_prompt)
    # print("\n下面是整体prompt：\n")
    # print(cleaned_logs)
    # print("\n2 完毕\n")

    # 5️ 让 Qwen 进行安全风险分析
    result = analyze_with_qwen(llm, cleaned_logs)
    # print(type(result))
    print("\n下面是大模型输出：\n")
    print(result)
    return result

if  __name__ == '__main__':
    log = 'IP: 127.0.0.1:8000'
    result = analyze_log(log)
    print(result)
