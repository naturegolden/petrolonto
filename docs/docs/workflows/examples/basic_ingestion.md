# 基础数据摄入

![](basic_ingestion.excalidraw.png)

创建如上所示的基础数据摄入工作流非常简单，请按照以下步骤操作：

1. 将 API 密钥添加到环境变量
```python
import os
os.environ["OPENAI_API_KEY"] = "myopenai_apikey"
```
查看我们的 `.env.example` 文件以了解可以配置的环境变量。PetrolOnto 支持 Anthropic、OpenAI 和 Mistral 的 API。还支持使用 Ollama 的本地模型。

2. 创建 YAML 文件 `basic_ingestion_workflow.yaml` 并将以下内容复制到其中
```yaml
parser_config:
  megaparse_config:
    strategy: "auto" # 对于 unstructured，可以是 "auto", "fast", "hi_res", "ocr_only"
    pdf_parser: "unstructured"
  splitter_config:
    chunk_size: 400 # 以令牌为单位
    chunk_overlap: 100 # 以令牌为单位
```

3. 使用上述配置和您要摄入的文件列表创建大脑
```python
from quivr_core import Brain
from quivr_core.config import IngestionConfig

config_file_name = "./basic_ingestion_workflow.yaml"

ingestion_config = IngestionConfig.from_yaml(config_file_name)

processor_kwargs = {
    "megaparse_config": ingestion_config.parser_config.megaparse_config,
    "splitter_config": ingestion_config.parser_config.splitter_config,
}

brain = Brain.from_files(name = "我的智能大脑",
                        file_paths = ["./我的第一个文档.pdf", "./我的第二个文档.txt"],
                        processor_kwargs=processor_kwargs,
                        )
```

4. 启动聊天
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

5. 现在您已经可以与大脑对话了，只需更改配置文件即可测试不同的分块策略！
