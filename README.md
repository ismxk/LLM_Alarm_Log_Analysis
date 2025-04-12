# log-rag 项目文档

## 项目介绍

**log-rag** 是一款网络服务日志告警系统，通过结合日志分析和信息检索技术，能够高效地处理、分析和告警服务日志。该系统利用大语言模型和向量数据库，帮助用户快速识别潜在问题并触发告警。

## 项目结构

项目包含了以下主要组件：

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

## 安装与使用

### 安装依赖

1. 克隆项目到本地：

```bash
git clone https://github.com/ismxk/LLM_Alarm_Log_Analysis.git
```

2. 安装项目依赖：

```bash
pip install -r requirements.txt
```

3. 启动 vllm 服务：

```bash
python -m vllm.entrypoints.api_server --model <模型路径或 Hugging Face 模型名称>
```

4. 启动 Gradio 前端界面：

```bash
python app.py
```

5. 访问 Gradio 服务，打开浏览器并访问以下地址：

```bash
http://127.0.0.1:7860
```

6. 运行实验脚本：

```bash
python experiment-v2.py
```

## 参与贡献
本项目由以下成员共同开发：

- Hanlin Tang：负责 Prompt Engineering、Langchain 项目框架搭建、Gradio 前端开发和实验设计。

- Haorong Zhang：负责检索数据整理、检索框架优化、检索模型微调、检索模型部署以及相关实验。

- Xiaokun Ma：负责 Qwen2.5 LoRA 微调、微调数据收集、微调模型部署、服务部署及微调实验。

## 如何贡献
欢迎社区成员参与到项目中来，贡献代码和提出问题。
Fork 该仓库：

1. 创建一个新的分支：git checkout -b feature/your-feature

2. 提交你的修改：git commit -am 'Add new feature'

3. 推送到分支：git push origin feature/your-feature

4. 创建一个 Pull Request，描述你的修改内容和目的。
