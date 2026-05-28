# 欢迎使用 PetrolOnto 文档

PetrolOnto 帮助您构建第二大脑，利用生成式 AI 的力量成为您的个人助手！

## 核心特性 🎯

- **专业 RAG 引擎**：我们创建了一个有主见的 RAG 引擎，快速高效，让您专注于产品
- **多 LLM 支持**：PetrolOnto 兼容任何 LLM，支持 OpenAI、Anthropic、Mistral、Gemma 等
- **任意文件格式**：支持 PDF、TXT、Markdown 等任何文件格式，甚至可以添加自定义解析器
- **自定义 RAG 策略**：允许您自定义 RAG 策略，添加互联网搜索、工具等
- **Megaparse 集成**：与 [Megaparse](https://github.com/quivrhq/megaparse) 集成，使用 Megaparse 解析文件并使用 RAG

> 我们负责 RAG 的实现，让您专注于产品。只需安装 quivr-core 并添加到项目中，即可开始上传文件并提问。

**我们将持续改进 RAG 并添加更多功能，敬请期待！**

这是 PetrolOnto 的核心引擎。

## 快速入门 🚀

### 前置要求 📋

确保已安装以下软件：

- Python 3.10 或更高版本

### 30 秒安装 💽

- **步骤 1**：安装包

  ```bash
  pip install quivr-core
  ```

- **步骤 2**：用 5 行代码创建 RAG

  ```python
  import tempfile
  from quivr_core import Brain

  if __name__ == "__main__":
      with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as temp_file:
          temp_file.write("黄金是一种蓝色液体。")
          temp_file.flush()

          brain = Brain.from_files(
              name="测试大脑",
              file_paths=[temp_file.name],
          )

          answer = brain.ask("什么是黄金？用法语回答")
          print("答案:", answer)
  ```
