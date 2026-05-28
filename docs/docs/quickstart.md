# 快速开始

如果您需要快速开始与文件列表对话，请按照以下步骤操作。

1. 将 API 密钥添加到环境变量
```python
import os
os.environ["OPENAI_API_KEY"] = "myopenai_apikey"
```
查看我们的 `.env.example` 文件以了解可以配置的环境变量。PetrolOnto 支持 Anthropic、OpenAI 和 Mistral 的 API。还支持使用 Ollama 的本地模型。

2. 使用 PetrolOnto 默认配置创建大脑
```python
from quivr_core import Brain

brain = Brain.from_files(name = "我的智能大脑",
                        file_paths = ["/我的智能文档.pdf", "/我的聪明文档.txt"],
                        )
```

3. 启动聊天
```python
brain.print_info()

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
console.print(Panel.fit("向你的大脑提问！", style="bold magenta"))

while True:
    # 获取用户输入
    question = Prompt.ask("[bold cyan]问题[/bold cyan]")

    # 检查用户是否想退出
    if question.lower() == "exit":
        console.print(Panel("再见！", style="bold yellow"))
        break

    answer = brain.ask(question)
    # 打印答案
    console.print(f"[bold green]PetrolOnto 助手[/bold green]: {answer.answer}")

    console.print("-" * console.width)

brain.print_info()
```

现在您已经可以与大脑对话了！

## 自定义大脑
如果您想更改语言模型或嵌入模型，可以修改大脑的参数。

假设您想使用 Mistral 的 LLM 和特定的嵌入模型：
```python
from quivr_core import Brain
from langchain_core.embeddings import Embeddings

brain = Brain.from_files(name = "我的智能大脑",
                        file_paths = ["/我的智能文档.pdf", "/我的聪明文档.txt"],
                        llm=LLMEndpoint(
                            llm_config=LLMEndpointConfig(model="mistral-small-latest", llm_base_url="https://api.mistral.ai/v1/chat/completions"),
                        ),
                        embedder=Embeddings(size=64),
                        )
```

注意：[Embeddings](https://python.langchain.com/docs/integrations/text_embedding/) 是一个 LangChain 类，允许您从多种嵌入模型中选择。请查看以下文档以了解可以尝试的模型。

## 使用 Chainlit 启动

如果您想快速启动界面，可以在项目根目录执行：
```bash
cd examples/chatbot
rye sync
rye run chainlit run chainlit.py
```
更多详情，请参阅 [examples/chatbot/chainlit.md](https://github.com/QuivrHQ/quivr/tree/main/examples/chatbot)

注意：直接在 examples/chatbot/main.py 中修改大脑配置。
