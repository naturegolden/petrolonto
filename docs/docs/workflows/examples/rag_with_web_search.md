# 带网络搜索的 RAG

![](rag_with_web_search.excalidraw.png)

请按照以下步骤创建如上所示的智能 RAG 工作流，它包含以下高级功能：

* **用户意图检测** - 代理可以检测用户是否希望激活网络搜索工具以查找文档中不存在的信息
* **动态块检索** - 检索的块数量不是固定的，而是根据重排器的相关性分数和用户提供的 `relevance_score_threshold` 动态确定
* **网络搜索** - 代理可以在需要时搜索网络获取更多信息

---

1. 将 API 密钥添加到环境变量
```python
import os
os.environ["OPENAI_API_KEY"] = "my_openai_api_key"
os.environ["TAVILY_API_KEY"] = "my_tavily_api_key"
```
查看我们的 `.env.example` 文件以了解可以配置的环境变量。PetrolOnto 支持 Anthropic、OpenAI 和 Mistral 的 API。还支持使用 Ollama 的本地模型。

2. 创建 YAML 文件 `rag_with_web_search_workflow.yaml` 并将以下内容复制到其中
```yaml
workflow_config:
  name: "带网络搜索的 RAG"

  # 代理可以在用户指令需要时激活的工具列表
  available_tools:
    - "web search"

  nodes:
    - name: "START"
      conditional_edge:
        routing_function: "routing_split"
        conditions: ["edit_system_prompt", "filter_history"]

    - name: "edit_system_prompt"
      edges: ["filter_history"]

    - name: "filter_history"
      edges: ["dynamic_retrieve"]

    - name: "dynamic_retrieve"
      conditional_edge:
        routing_function: "tool_routing"
        conditions: ["run_tool", "generate_rag"]

    - name: "run_tool"
      edges: ["generate_rag"]

    - name: "generate_rag" # 最后一个节点的名称，我们从中向用户流式传输答案
      edges: ["END"]
      tools:
        - name: "cited_answer"

# 包含在答案上下文中的最大历史对话迭代次数
max_history: 10

# 检索器返回的块数
k: 40

# 重排器配置
reranker_config:
  # 要使用的重排器供应商
  supplier: "cohere"

  # 用于给定供应商的重排器模型
  model: "rerank-multilingual-v3.0"

  # 重排器返回的块数
  top_n: 5

  # 在重排器返回的块中，只有相关性分数等于或高于 relevance_score_threshold 的块才会返回给 LLM 生成答案（允许的值在 0 到 1 之间，0.1 的值适用于 cohere 和 jina 重排器）
  relevance_score_threshold: 0.01

# LLM 配置
llm_config:

  # 传递给 LLM 生成答案的最大令牌数
  max_input_tokens: 8000

  # LLM 的温度
  temperature: 0.7
```

3. 使用默认配置创建大脑
```python
from quivr_core import Brain

brain = Brain.from_files(name = "我的智能大脑",
                        file_paths = ["./我的第一个文档.pdf", "./我的第二个文档.txt"],
                        )
```

4. 启动聊天
```python
brain.print_info()

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from quivr_core.config import RetrievalConfig

config_file_name = "./rag_with_web_search_workflow.yaml"

retrieval_config = RetrievalConfig.from_yaml(config_file_name)

console = Console()
console.print(Panel.fit("向你的大脑提问！", style="bold magenta"))

while True:
    # 获取用户输入
    question = Prompt.ask("[bold cyan]问题[/bold cyan]")

    # 检查用户是否想退出
    if question.lower() == "exit":
        console.print(Panel("再见！", style="bold yellow"))
        break

    answer = brain.ask(question, retrieval_config=retrieval_config)
    # 打印答案
    console.print(f"[bold green]PetrolOnto 助手[/bold green]: {answer.answer}")

    console.print("-" * console.width)

brain.print_info()
```

5. 现在您已经可以与大脑对话了，只需更改配置文件即可测试不同的检索策略！
