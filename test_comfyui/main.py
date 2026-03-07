from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper

# 连接本地的ComfyUI
api = ComfyApiWrapper("http://10.168.1.206:8188/")
# 加载你的API格式工作流
wf = ComfyWorkflowWrapper("video_ltx2_3_t2v.json")

# 假设你有一个prompts列表
prompts = ["中国古装片，武侠，剑客对战", "权利的游戏，私生子之战"]
for i, prompt_text in enumerate(prompts):
    # 修改工作流中提示词节点的内容（节点标题需事先设置为唯一名称）
    wf.set_node_param("CLIP文本编码pos", "text", prompt_text)
    # 提交任务并等待结果
    results = api.queue_and_wait_images(wf, "保存视频")
    # 保存图片
    for filename, video_data in results.items():
        print("filename:", filename)
        with open(f"output_{i}_{filename}", "wb+") as f:
            f.write(video_data)
