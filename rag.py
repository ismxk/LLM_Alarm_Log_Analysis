from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema.document import Document
import config

# 初始化 Chroma 向量数据库
def load_vectorstore():
    """加载或创建 Chroma 向量数据库"""
    return Chroma(persist_directory=config.VECTOR_DB_PATH, embedding_function=OpenAIEmbeddings())

# 获取 RAG 检索器
vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever()

def search_logs(query):
    """查询 RAG 向量数据库，返回相关日志"""
    retrieved_docs = retriever.get_relevant_documents(query)
    return "\n".join([doc.page_content for doc in retrieved_docs])
