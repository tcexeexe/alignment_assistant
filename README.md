## API接口调用说明

### 请求头（Headers）

- **Content-Type:** `application/json`
- **Authorization:** `Bearer {token}`

### 请求体（Body）

请求体应该是JSON格式，包含以下字段：

- **model:** 字符串类型，指定使用的模型名称，这里是`"RLHF"`。

- **messages:** 一个包含字典的列表，每个字典代表一条消息，包含以下字段：
  - **role:** 字符串类型，指定消息的角色，这里是`"user"`。
  - **question:** 字符串类型，经过加密的用户问题。
  - **answer:** 字符串类型，经过加密的答案。
  - **stop:** 一个列表，用于指定停止词或特殊标记。在这个例子中为空，但可以在此处添加自定义的停止词。

### 示例请求体

```json
{
  "model": "RLHF",
  "messages": [
    {
      "role": "user",
      "question": "加密后的问题",
      "answer": "加密后的答案",
      "stop": []
    }
  ]
}
