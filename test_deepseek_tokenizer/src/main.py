# encoding: utf-8

import transformers
# encoding/encoding_dsv32.py
from encoding_dsv32 import encode_messages, parse_message_from_completion_text

tokenizer = transformers.AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-V3.2")

messages = [
    {"role": "user", "content": "hello"},
    {"role": "assistant", "content": "Hello! I am DeepSeek.", "reasoning_content": "thinking..."},
    {"role": "user", "content": "1+1=?"}
]
encode_config = dict(thinking_mode="thinking", drop_thinking=True, add_default_bos_token=True)

# messages -> string
prompt = encode_messages(messages, **encode_config)
# Output: "<｜begin▁of▁sentence｜><｜User｜>hello<｜Assistant｜></think>Hello! I am DeepSeek.<｜end▁of▁sentence｜><｜User｜>1+1=?<｜Assistant｜><think>"

#prompt = "你好，这是一段测试文本"
#print(tokenizer.tokenize("hello, this is a testing text"))

# string -> tokens
tokens = tokenizer.encode(prompt)
# Output: [0, 128803, 33310, 128804, 128799, 19923, 3, 342, 1030, 22651, 4374, 1465, 16, 1, 128803, 19, 13, 19, 127252, 128804, 128798]
print(tokens)
print(tokenizer.decode(tokens))


