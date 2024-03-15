帮助LLM模型进行RLHF微调，提供API接口调用。
API接口调用格式：


请求头（Headers）：
- Content-Type: application/json
- Authorization: Bearer {token}

请求体（Body）：JSON格式，包含以下字段：
model: 字符串，指定使用的模型名称，这里是"RLHF"。
messages: 一个包含字典的列表，每个字典代表一条消息，包含以下字段：
    role: 字符串，指定消息的角色，这里是"user"。
    question: 字符串，经过加密的用户问题。
    answer: 字符串，经过加密的答案。
    stop: 一个列表，用于指定停止词或特殊标记（在这个例子中为空，但注释提到了可以在此处添加自定义的停止词）。
