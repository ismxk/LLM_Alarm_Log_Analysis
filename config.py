# 配置文件
# OLLAMA_MODEL = "qwen"  # Ollama 本地部署的 Qwen 模型
#原始Qwen2.5-7B-Instruct
#MODEL7B_PATH = "/root/.cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots/a09a35458c702b33eeacc393d103063234e8bc28"
MODEL7B_PATH = "Qwen/Qwen2.5-7B-Instruct"
#原始Qwen2.5-32B-Instruct
MODEL32B_PATH = "/root/.cache/huggingface/hub/models--Qwen--Qwen2.5-32B-Instruct/snapshots/5ede1c97bbab6ce5cda5812749b4c0bdf79b18dd"
#MODEL32B_PATH = "Qwen/Qwen2.5-32B-Instruct"

#微调后的Qwen2.5-7B-Instruct适配器
LORA_MODEL7B_PATH = "/work/home/acptye74du/LLaMA-Factory/saves/Qwen2.5-7B-Instruct/train_2025-02-17"

#微调后的Qwen2.5-32B-Instruct适配器
LORA_MODEL32B_PATH = "/work/home/acptye74du/LLaMA-Factory/saves/Qwen2.5-32B-Instruct/train_2025-02-22"

#嵌入模型的路径
EMBEDDING_MD_PATH = "/work/home/acptye74du/log-rag-master/embedding_model"

# 向量数据库存储路径
VECTOR_DB_PATH = "/work/home/acptye74du/log-rag-master/database/VECTOR_DB"

# SQLite 日志存储数据库
SQLITE_DB_PATH = "/work/home/acptye74du/log-rag-master/database/SQLITE_DB"
