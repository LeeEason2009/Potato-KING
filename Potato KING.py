import requests

# 配置不同模型的 API 密钥和基础 URL
API_CONFIG = {
    "openai": {
        "api_key": "YOUR_OPENAI_API_KEY",  # 替换为你的 OpenAI API 密钥
        "base_url": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-3.5-turbo"
    },
    "deepseek": {
        "api_key": "YOUR_DEEPSEEK_API_KEY",  # 替换为你的 DeepSeek API 密钥
        "base_url": "https://api.deepseek.com/v1/chat",
        "model": "DeepSeek-V3"
    },
    "kimi": {
        "api_key": "YOUR_KIMI_API_KEY",  # 替换为你的 Kimi API 密钥
        "base_url": "https://api.kimi.com/v1/chat",
        "model": "kimi-1.5"
    },
    "doubao": {
        "api_key": "YOUR_DOUBAO_API_KEY",  # 替换为你的 Doubao API 密钥
        "base_url": "https://api.doubao.com/v1/chat",
        "model": "doubao-v1"
    }
}

# 图像生成 API 配置（示例：使用 DALL·E）
IMAGE_GEN_CONFIG = {
    "api_key": "YOUR_DALL_E_API_KEY",  # 替换为你的 DALL·E API 密钥
    "base_url": "https://api.openai.com/v1/images/generations",
    "model": "dall-e-3"
}

# 音乐问答 API 配置（示例：使用 DeepSeek）
MUSIC_QA_CONFIG = {
    "api_key": "YOUR_DEEPSEEK_API_KEY",  # 替换为你的 DeepSeek API 密钥
    "base_url": "https://api.deepseek.com/v1/music",
    "model": "DeepSeek-Music"
}

# 通用的 API 调用函数
def call_api(provider, prompt):
    config = API_CONFIG.get(provider)
    if not config:
        print(f"土豆King：不支持的模型提供商 '{provider}'")
        return None

    headers = {"Authorization": f"Bearer {config['api_key']}", "Content-Type": "application/json"}
    data = {"model": config["model"], "messages": [{"role": "user", "content": prompt}]}

    try:
        response = requests.post(config["base_url"], headers=headers, json=data)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"土豆King：调用 {provider} API 时出错：{e}")
        return None

# 图像生成函数
def generate_image(prompt):
    headers = {"Authorization": f"Bearer {IMAGE_GEN_CONFIG['api_key']}", "Content-Type": "application/json"}
    data = {"model": IMAGE_GEN_CONFIG["model"], "prompt": prompt, "n": 1, "size": "512x512"}

    try:
        response = requests.post(IMAGE_GEN_CONFIG["base_url"], headers=headers, json=data)
        response.raise_for_status()
        image_url = response.json()["data"][0]["url"]
        print(f"土豆King：生成的图像链接：{image_url}")
        return image_url
    except requests.exceptions.RequestException as e:
        print(f"土豆King：图像生成失败：{e}")
        return None

# 音乐问答函数
def music_qa(prompt):
    headers = {"Authorization": f"Bearer {MUSIC_QA_CONFIG['api_key']}", "Content-Type": "application/json"}
    data = {"model": MUSIC_QA_CONFIG["model"], "messages": [{"role": "user", "content": prompt}]}

    try:
        response = requests.post(MUSIC_QA_CONFIG["base_url"], headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"土豆King：音乐问答失败：{e}")
        return None

# 土豆King：主程序
def main():
    print("土豆King：欢迎使用集成式泛用性 AI！")
    language = input("请选择语言 (1. 中文 / 2. English): ").strip()
    if language == "1":
        prompt = input("请输入您的问题或指令：")
    elif language == "2":
        prompt = input("Please enter your question or command: ")
    else:
        print("土豆King：无效的语言选择，已默认切换到中文。")
        prompt = input("请输入您的问题或指令：")

    if "画" in prompt or "generate image" in prompt.lower():
        image_url = generate_image(prompt)
        if image_url:
            print(f"土豆King：生成的图像链接：{image_url}")
    elif "音乐" in prompt or "music" in prompt.lower():
        response = music_qa(prompt)
        if response:
            print(f"土豆King：音乐问答结果：{response}")
    else:
        providers = list(API_CONFIG.keys())  # 获取所有支持的模型提供商
        print(f"土豆King：正在调用多个 AI 模型来回答您的问题...")
        for provider in providers:
            result = call_api(provider, prompt)
            if result:
                response_text = result.get("choices", [{}])[0].get("message", {}).get("content", "无响应")
                if language == "2":
                    print(f"土豆King：Response from {provider.capitalize()}:\n{response_text}\n")
                else:
                    print(f"土豆King：{provider.capitalize()} 的回答：\n{response_text}\n")
            else:
                if language == "2":
                    print(f"土豆King：No valid response from {provider.capitalize()}.\n")
                else:
                    print(f"土豆King：{provider.capitalize()} 未返回有效结果。\n")

if __name__ == "__main__":
    main()