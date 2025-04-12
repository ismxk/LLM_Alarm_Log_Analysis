# from langchain_community.llms import ChatOllama
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
from peft import PeftModel  # 确保已安装peft库：pip install peft
from vllm import LLM, SamplingParams
import config


def vllm_init(model_path, adapter_path=None):
    # tokenizer = AutoTokenizer.from_pretrained(model_path,
    #                                           trust_remote_code=True)
    # model = AutoModelForCausalLM.from_pretrained(model_path,
    #                                                 device_map="auto",
    #                                                 trust_remote_code=True).eval()
    model = LLM(model=model_path, gpu_memory_utilization=0.95, max_model_len=8192)
    # 加载LoRA适配器
    if adapter_path:
        model = PeftModel.from_pretrained(
            model,
            adapter_path  # 指定LoRA适配器路径
        )
    return model


# # 定义生成参数
#     sampling_params = SamplingParams(temperature=0.7, top_p=0.9, max_tokens=100)
#     return llm
        

def init_llm(model_path, adapter_path=None):
    # 配置 8-bit 量化
    quantization_config = BitsAndBytesConfig(
        load_in_8bit=True,  # 启用 8-bit 量化
        llm_int8_threshold=6.0,  # 设置量化阈值
    )
    tokenizer = AutoTokenizer.from_pretrained(model_path,
                                              trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path,
                                                    device_map="auto",
                                                 torch_dtype='auto',
                                                 use_flash_attention_2=True,
                                                 quantization_config=quantization_config,  # 应用量化配置
                                                    trust_remote_code=True).eval()
    # load_in_8bit=True, 
    # 加载LoRA适配器
    if adapter_path:
        model = PeftModel.from_pretrained(
            model,
            adapter_path  # 指定LoRA适配器路径
        )
        # 可选：合并适配器到基础模型（合并后推理更快，但无法继续训练）
        #model = model.merge_and_unload()
        #         return_full_text=False,
    
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        # max_length=4096,
        # max_tokens=1048,
        max_new_tokens=200,
        top_p=4,
        return_full_text=False,
        repetition_penalty=1.5
    )
    llm = HuggingFacePipeline(pipeline=pipe)
    
    # return model, tokenizer
    return llm

def init_peft_llm(model_path, adapter_path=None):
    tokenizer = AutoTokenizer.from_pretrained(model_path,
                                              trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path,
                                                    device_map="auto",
                                                    trust_remote_code=True).eval()
    # load_in_8bit=True, 
    # 加载LoRA适配器
    if adapter_path:
        model = PeftModel.from_pretrained(
            model,
            adapter_path  # 指定LoRA适配器路径
        )
        # 可选：合并适配器到基础模型（合并后推理更快，但无法继续训练）
        #model = model.merge_and_unload()
    
    # pipe = pipeline(
    #     "text-generation",
    #     model=model,
    #     tokenizer=tokenizer,
    #     # max_length=4096,
    #     # max_tokens=4096,
    #     max_new_tokens=2048,
    #     top_p=1,
    #     repetition_penalty=1.15
    # )
    # llm = HuggingFacePipeline(pipeline=pipe)
    
    return model, tokenizer

def peft_llm_generate(model, tokenizer, input_text):
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

    # 生成文本
    outputs = model.generate(
        **inputs,
        max_length=1024,
        num_return_sequences=1,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
    )
    
    # 解码输出
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text


def generate_query_peft(model, tokenizer, log_entry):
    from prompts import prompt1
    query_prompt = prompt1.format(log_entry=log_entry)
    query = peft_llm_generate(model, tokenizer, query_prompt)

def analyze_peft(model, tokenizer, formatted_prompt):
    result = peft_llm_generate(model,tokenizer, formatted_prompt)
    return result

def generate_query_with_qwen(llm, log_entry):
    """调用 Qwen 生成 RAG 检索的查询关键词"""
    from prompts import prompt1
    query_prompt = prompt1.format(log_entry=log_entry)
    return llm.invoke(query_prompt)
    # return llm.generate(query_prompt)


def analyze_with_qwen(llm, formatted_prompt):
    """调用 Qwen 进行日志安全分析"""
    return llm.invoke(formatted_prompt)
    # return llm.generate(formatted_prompt)


if __name__ == '__main__':
    model_path = config.MODEL32B_PATH
    adapter_path = config.LORA_MODEL32B_PATH
    #微调后
    llm = init_llm(model_path, adapter_path)
    #微调前
    #llm = init_llm(model_path)
    query = generate_query_with_qwen(llm, "2023-10-11 00:00:00")
    print('1: '+query)
    risk = analyze_with_qwen(llm, "2023-10-11 00:00:00")
    print('2: '+risk)