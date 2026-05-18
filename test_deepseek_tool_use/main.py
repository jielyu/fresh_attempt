import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TOKEN = os.getenv("TOKEN")

client = OpenAI(
    api_key=TOKEN,
    base_url="https://api.deepseek.com",
)

# 定义一个简单的测试工具：打印测试字符串
tools = [
    {
        "type": "function",
        "function": {
            "name": "print_test_string",
            "description": "打印一个测试字符串，用于验证工具调用功能是否正常工作",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "要打印的测试消息",
                    }
                },
                "required": ["message"],
            },
        },
    }
]


def print_test_string(message: str) -> str:
    """工具函数：打印测试字符串"""
    print(f"[工具调用] 测试字符串: {message}")
    return f"已成功打印测试字符串: {message}"


def run():
    print("=== DeepSeek 工具调用（Tool Use）完整示例 ===\n")

    system_prompt = (
        "你是一个测试工具调用功能的助手。"
        "当用户要求打印消息时，你必须使用 print_test_string 工具逐条完成，每次只打印一条。"
        "完成所有工具调用后，向用户总结你完成了哪些操作。"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "请帮我依次调用 print_test_string 工具打印以下三条消息：\n"
                "1. 'Hello, DeepSeek Tool Use!'\n"
                "2. '这是第二次工具调用'\n"
                "3. '这是第三次工具调用'\n"
                "请每次只打印一条，分三次调用工具完成。"
            ),
        },
    ]

    max_turns = 10
    turn = 0

    while turn < max_turns:
        turn += 1
        print(f"--- 第 {turn} 轮 ---")
        print("发送消息到 DeepSeek API...")

        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=messages,
            tools=tools,
        )

        message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason
        print(f"finish_reason = {finish_reason}")

        # 停止条件：模型不再请求调用工具
        if finish_reason != "tool_calls":
            print(f"\n模型最终回复: {message.content}")
            break

        # 模型请求调用工具
        print(f"模型请求 {len(message.tool_calls)} 个工具调用:")
        for tc in message.tool_calls:
            print(f"  - id: {tc.id}")
            print(f"    function: {tc.function.name}")
            print(f"    arguments: {tc.function.arguments}")

        # 将包含 tool_calls 的模型回复加入消息历史
        messages.append(message.model_dump())

        # 依次执行每个工具调用
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            if func_name == "print_test_string":
                result = print_test_string(**func_args)
            else:
                result = f"未知工具: {func_name}"

            # 将工具执行结果加入消息历史
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

        print()

    if turn >= max_turns:
        print("⚠️ 达到最大轮次限制，强制停止")

    print("=== 完整轮回结束 ===")


if __name__ == "__main__":
    run()
