## 聊天历史（ChatHistory）

`ChatHistory` 类是存储用户与 LLM 之间所有对话的地方。每次创建 `Brain` 时，都会透明地实例化一个 `ChatHistory` 对象。

在每次使用 `Brain.ask_streaming` 交互时，您的消息和 LLM 的响应都会被添加到聊天历史中。这非常方便，因为这个历史在检索增强生成（RAG）过程中用于为 LLM 提供更多上下文，作为用户与系统之间的记忆形式，通过查看已经说过的内容帮助 LLM 生成更好的响应。

您还可以通过 `print_info()` 方法打印大脑的详细信息，获取关于大脑的一些信息，例如存储了多少聊天、当前聊天历史等。这使得跟踪对话内容和管理发送到 LLM 的上下文变得非常简单！

::: quivr_core.rag.entities.chat
    options:
      heading_level: 2
