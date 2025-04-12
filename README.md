# log-rag

#### 介绍
网络服务日志告警系统

#### 软件架构
log_alert_system/
│── app.py                  # 主程序，运行 Gradio 前端
│── config.py               # 配置文件（数据库、本地模型等）
│── prompts.py              # 存放 Prompt1 和 Prompt2
│── rag.py                  # RAG 检索系统（向量数据库存储）
│── model.py                # 本地 Qwen 大模型推理
│── log_analyzer.py         # 核心日志分析逻辑
│── experiment-v2.py        # 实验代码
│── retrieval.py            # 检索代码
│── requirements.txt        # 依赖包列表

#### 安装&使用
1.  clone项目到本地
2.  安装依赖：pip install -r requirements.txt
3.  启动vllm服务：python -m vllm.entrypoints.api_server --model <模型路径或Hugging Face模型名称>
4.  运行Gradio：python app.py
5.  访问服务：http://127.0.0.1:7860
6.  运行实验 python experiment-v2.py

#### 参与贡献
*  Hanlin Tang：Prompt Engineering，Langchain项目框架搭建，Gradio前端开发，实验设计
*  Haorong Zhang：检索数据整理，检索框架优化，检索模型微调，检索模型部署，检索实验
*  Xiaokun Ma：Qwen2.5 LoRA微调，微调数据收集，微调模型部署，服务部署，微调实验
