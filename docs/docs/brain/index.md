# 🧠 大脑

大脑是 PetrolOnto 的核心组件，用于存储和处理您想要检索信息的知识。只需使用您想要处理的文件创建大脑，然后使用最新的 PetrolOnto RAG 工作流从知识中检索信息。

快速开始 🪄：

```python
from quivr_core import Brain
from quivr_core.quivr_rag_langgraph import QuivrQARAGLangGraph


brain = Brain.from_files(name="我的大脑", file_paths=["file1.pdf", "file2.pdf"])
answer = brain.ask("什么是 PetrolOnto？")
print("PetrolOnto 回答：", answer.answer)

```

定制你的大脑 🔨：

```python
from quivr_core import Brain
from quivr_core.llm.llm_endpoint import LLMEndpoint
from quivr_core.embedder.embedder import DeterministicFakeEmbedding
from quivr_core.llm.llm_endpoint import LLMEndpointConfig
from quivr_core.llm.llm_endpoint import FakeListChatModel

brain = Brain.from_files(
        name="测试大脑",
        file_paths=["我的信息源文件.pdf"],
        llm=LLMEndpoint(
            llm=FakeListChatModel(responses=["好的"]),
            llm_config=LLMEndpointConfig(model="fake_model", llm_base_url="local"),
        ),
        embedder=DeterministicFakeEmbedding(size=20),
    )

answer = brain.ask(
            "什么是 PetrolOnto？"
        )
print("PetrolOnto 回答：", answer.answer)

```
