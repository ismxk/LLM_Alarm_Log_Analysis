import gradio as gr
from log_analyzer import analyze_log


# Gradio 交互界面
def gradio_interface(log_entry):
    print('接收输入'+log_entry)
    response = analyze_log(log_entry)
    print("输出"+response)
    return response


# 启动 Gradio
if __name__ == "__main__":
    # 创建 Gradio UI
    iface = gr.Interface(
        fn=gradio_interface,
        inputs=gr.Textbox(lines=5, placeholder="请输入日志内容", label='log_enrty'),
        outputs="text",
        title="日志自动告警系统",
        description="输入服务器访问日志，系统将自动分析是否存在安全风险。",
    )
    # dashboard.launch(share=True)
    iface.launch(share=True)
    # gradio_interface('abc')
