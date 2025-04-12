import pandas as pd
from model import init_llm
import config

#from log_analyzer import analyze_log
from log_analyzer_test import analyze_log
from log_analyzer_no_rag import analyze_log_norag

def experiment(test_data='./test.csv'):
    #print(1)
    #return
    df =  pd.read_csv(test_data)
    #原始Qwen2.5-7B-Instruct模型
    model_path = config.MODEL32B_PATH
    #微调后的Qwen2.5-7B-Instruct lora适配器
    adapter_path = config.LORA_MODEL32B_PATH
    #微调前
    llm = init_llm(model_path)
    results = []
    for i, row in df.iterrows():
        format_str = f'code: {row['response_code']}\n response: {row['response']}\n payload: {row['request_payload']}'
        result = analyze_log_norag(format_str, llm)
        results.append(result)
    df['llm_output'] = results
    df.to_csv('./微调前_无rag_output_32b.csv')

def experiment2(test_data='./test.csv'):
    #print(2)
    #return
    df =  pd.read_csv(test_data)
    #原始Qwen2.5-7B-Instruct模型
    model_path = config.MODEL7B_PATH
    #微调后的Qwen2.5-7B-Instruct lora适配器
    adapter_path = config.LORA_MODEL7B_PATH
    #微调后
    llm = init_llm(model_path, adapter_path)
    results = []
    for i, row in df.iterrows():
        print(i)
        format_str = f'code: {row['response_code']}\n response: {row['response']}\n payload: {row['request_payload']}'
        result = analyze_log_norag(format_str, llm)
        results.append(result)
    df['llm_output'] = results
    df.to_csv('./微调后_无rag_output.csv')

def experiment3(test_data='./test.csv'):
    #print(3)
    #return
    df =  pd.read_csv(test_data)
    #原始Qwen2.5-7B-Instruct模型
    model_path = config.MODEL7B_PATH
    #微调后的Qwen2.5-7B-Instruct lora适配器
    adapter_path = config.LORA_MODEL7B_PATH
    llm = init_llm(model_path)
    results = []
    for i, row in df.iterrows():
        print(i)
        format_str = f'code: {row['response_code']}\n response: {row['response']}\n payload: {row['request_payload']}'
        result = analyze_log(format_str, llm)
        results.append(result)
    df['llm_output'] = results
    df.to_csv('./微调前_有rag_output.csv')

def experiment4(test_data='./test.csv'):
    #print(4)
    df =  pd.read_csv(test_data)
    #原始Qwen2.5-7B-Instruct模型
    model_path = config.MODEL32B_PATH
    #微调后的Qwen2.5-7B-Instruct lora适配器
    adapter_path = config.LORA_MODEL32B_PATH
    #微调后
    llm = init_llm(model_path, adapter_path)
    results = []
    for i, row in df.iterrows():
        print(i)
        format_str = f'code: {row['response_code']}\n response: {row['response']}\n payload: {row['request_payload']}'
        result = analyze_log(format_str, llm)
        results.append(result)
    df['llm_output'] = results
    df.to_csv('./微调后_有rag_output_32b.csv')



if __name__ == '__main__':
    # experiment()
    #experiment2()
    # experiment3()
    experiment4()
