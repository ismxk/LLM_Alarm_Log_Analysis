import string
import json
from model import generate_query_with_qwen, analyze_with_qwen, init_llm
from prompts import prompt3
import config
from retrieval import search
from create_embedding_base import EmbeddingModel
import re
# from rag import search_logs
# import storage

def analyze_log_norag(log_entry, llm):
    """日志分析核心流程"""

    # 4️ 构建 Qwen 分析 Prompt
    formatted_prompt = prompt3.format(log_entry=log_entry)
    cleaned_logs = re.sub(r'[\?§©¨µè]{2,}', '', formatted_prompt)
    # print("\n下面是整体prompt：\n")
    # print(cleaned_logs)
    # print("\n完毕\n")

    # 5️ 让 Qwen 进行安全风险分析
    result = analyze_with_qwen(llm, cleaned_logs)
    print("\n下面是大模型输出：\n")
    print(result)
    return result

if  __name__ == '__main__':
    log = 'IP: 127.0.0.1:8000'
    result = analyze_log(log)
    print(result)
