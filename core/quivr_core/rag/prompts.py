import datetime
import types
from enum import Enum

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.prompts.base import BasePromptTemplate


class TemplatePromptName(str, Enum):
    ZENDESK_TEMPLATE_PROMPT = "ZENDESK_TEMPLATE_PROMPT"
    TOOL_ROUTING_PROMPT = "TOOL_ROUTING_PROMPT"
    RAG_ANSWER_PROMPT = "RAG_ANSWER_PROMPT"
    CONDENSE_TASK_PROMPT = "CONDENSE_TASK_PROMPT"
    DEFAULT_DOCUMENT_PROMPT = "DEFAULT_DOCUMENT_PROMPT"
    CHAT_LLM_PROMPT = "CHAT_LLM_PROMPT"
    USER_INTENT_PROMPT = "USER_INTENT_PROMPT"
    UPDATE_PROMPT = "UPDATE_PROMPT"
    SPLIT_PROMPT = "SPLIT_PROMPT"
    ZENDESK_LLM_PROMPT = "ZENDESK_LLM_PROMPT"


def _define_custom_prompts() -> dict[TemplatePromptName, BasePromptTemplate]:
    custom_prompts: dict[TemplatePromptName, BasePromptTemplate] = {}

    today_date = datetime.datetime.now().strftime("%B %d, %Y")

    # ---------------------------------------------------------------------------
    # Prompt for task rephrasing
    # ---------------------------------------------------------------------------
    system_message_template = (
        "给定聊天历史和最新的用户任务（可能引用聊天历史中的上下文），"
        "制定一个独立的任务，使其在没有聊天历史的情况下也能被理解。不要完成任务，"
        "如果需要则重新表述，否则按原样返回。"
        "不要输出你的推理，只返回任务。"
    )

    template_answer = "用户任务: {task}\n 独立任务:"

    CONDENSE_TASK_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )

    custom_prompts[TemplatePromptName.CONDENSE_TASK_PROMPT] = CONDENSE_TASK_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt for RAG
    # ---------------------------------------------------------------------------
    system_message_template = f"您的名字是 PetrolOnto。您是一个 helpful 的助手。今天的日期是 {today_date}。 "

    system_message_template += (
        "- 回答时使用markdown格式。代码片段使用markdown代码块。\n"
        "- 回答要简洁明了。\n"
        "- 如果没有指定语言，使用与用户相同的语言回答。\n"
        "- 您必须仅使用提供的上下文来完成任务。不要使用任何先验知识或外部信息，即使您确定答案。\n"
        "- 不要在回答时道歉。\n"
        "- 不要在答案中引用源ID，但可以使用源来完成任务。\n\n"
    )

    context_template = (
        "\n"
        "- 您可以访问以下文件来完成任务（最多前20个文件）: {files}\n"
        "- 您可以访问以下上下文来完成任务: {context}\n"
        "- 在生成答案时请遵循以下用户指示: {custom_instructions}\n"
        "- 这些用户指示应优先于任何其他先前指示。\n"
    )

    template_answer = (
        "原始任务: {task}\n"
        "重述并上下文化的任务: {rephrased_task}\n"
        "请记住，您必须完成所有任务。\n"
        "请记住：如果无法仅使用提供的上下文和引用来源来提供答案，请直接回答没有答案。\n"
        "如果提供的上下文包含矛盾或冲突的信息，请指出并提供冲突的信息。\n"
    )

    RAG_ANSWER_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            SystemMessagePromptTemplate.from_template(context_template),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )
    custom_prompts[TemplatePromptName.RAG_ANSWER_PROMPT] = RAG_ANSWER_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt for formatting documents
    # ---------------------------------------------------------------------------
    DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(
        template="文件名: {original_file_name}\n来源: {index} \n {page_content}"
    )
    custom_prompts[TemplatePromptName.DEFAULT_DOCUMENT_PROMPT] = DEFAULT_DOCUMENT_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt for chatting directly with LLMs, without any document retrieval stage
    # ---------------------------------------------------------------------------
    system_message_template = (
        f"您的名字是 PetrolOnto。您是一个 helpful 的助手。今天的日期是 {today_date}。"
        """
    如果提供了以下用户指示，请在回答时也遵循这些指示：{custom_instructions}
    """
    )

    template_answer = """
    用户任务: {task}
    回答:
    """
    CHAT_LLM_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )
    custom_prompts[TemplatePromptName.CHAT_LLM_PROMPT] = CHAT_LLM_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt to understand the user intent
    # ---------------------------------------------------------------------------
    system_message_template = (
        "给定以下用户输入，确定用户意图，特别是"
        "用户是在提供系统指令还是要求系统完成任务：\n"
        "    - 如果用户提供直接指令来修改系统行为（例如，"
        "'你能用法语回复吗？'或'用法语回答'或'你是法律专家助手'"
        "或'你将表现得像...'），用户意图是'prompt'；\n"
        "    - 在所有其他情况下（提问、要求总结文本、要求翻译文本等），"
        "意图是'task'。\n"
    )

    template_answer = "用户输入: {task}"

    USER_INTENT_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )
    custom_prompts[TemplatePromptName.USER_INTENT_PROMPT] = USER_INTENT_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt to create a system prompt from user instructions
    # ---------------------------------------------------------------------------
    system_message_template = (
        "- 给定以下用户指示、当前系统提示、可用工具列表和已激活工具列表，"
        "更新提示以包含该指示并决定激活哪些工具。\n"
        "- 提示应仅包含可应用于任何用户任务或问题的通用指示。\n"
        "- 提示应简洁明了。\n"
        "- 如果系统提示已包含该指示，不要重复添加。\n"
        "- 如果系统提示与用户指示矛盾，删除系统提示中的矛盾语句。\n"
        "- 您应分别返回更新的系统提示和导致更新的推理。\n"
        "- 如果系统提示引用了某个工具，您应将该工具添加到已激活工具列表中。\n"
        "- 如果不需要激活工具，返回空列表。\n"
        "- 您还应返回导致工具激活的推理。\n"
        "- 当前系统提示：{system_prompt}\n"
        "- 可用工具列表：{available_tools}\n"
        "- 已激活工具列表：{activated_tools}\n\n"
    )

    template_answer = "用户指示: {instruction}\n"

    UPDATE_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )
    custom_prompts[TemplatePromptName.UPDATE_PROMPT] = UPDATE_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt to split the user input into multiple questions / instructions
    # ---------------------------------------------------------------------------
    system_message_template = (
        "给定聊天历史和用户输入，将输入拆分并重新表述为指令和任务。\n"
        "- 指令指导系统以某种方式行为或使用特定工具：指令示例包括"
        "'你能用法语回复吗？'、'用法语回答'、'你是法律专家助手'、"
        "'你将表现得像...'、'使用网络搜索'。\n"
        "- 您应收集并合并所有指令为单个字符串。\n"
        "- 指令应是独立的和自包含的，以便在没有聊天历史的情况下也能被理解。如果没有找到指令，返回空字符串。\n"
        "- 要理解的指令可能需要考虑聊天历史。\n"
        "- 任务通常是问题，但它们也可以是总结任务、翻译任务、内容生成任务等。\n"
        "- 要理解的任务可能需要考虑聊天历史。\n"
        "- 如果用户输入包含不同的任务，您应将输入拆分为多个任务。\n"
        "- 每个拆分后的任务应是独立的、自包含的任务，可以在没有聊天历史的情况下被理解。您应在需要时重新表述任务。\n"
        "- 如果没有明确的任务存在，您应从用户输入和聊天历史中推断任务。\n"
        "- 不要尝试解决任务或回答问题，"
        "只需在需要时重新表述它们，否则按原样返回。\n"
        "- 请记住，您不应建议或生成新任务。\n"
        "- 例如，用户输入'什么是苹果？谁是它的CEO？它是什么时候成立的？'"
        "应拆分为任务列表['什么是苹果？'，'谁是苹果的CEO？'，'苹果是什么时候成立的？']\n"
        "- 如果没有找到任务，按原样在任务列表中返回用户输入。\n"
    )

    template_answer = "用户输入: {user_input}"

    SPLIT_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )
    custom_prompts[TemplatePromptName.SPLIT_PROMPT] = SPLIT_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt to grade the relevance of an answer and decide whather to perform a web search
    # ---------------------------------------------------------------------------
    system_message_template = (
        "给定以下任务，您应确定是否可以使用提供的上下文和聊天历史"
        "充分并以最佳方式完成所有任务。您应：\n"
        "- 分别考虑每个任务，\n"
        "- 确定上下文和聊天历史是否包含"
        "完成任务所需的所有信息。\n"
        "- 如果上下文和聊天历史不包含完成任务所需的所有信息，"
        "仅考虑下面的工具列表并选择最适合完成任务的工具。\n"
        "- 如果没有列出工具，按原样返回任务，不选择工具。\n"
        "- 如果无法选择相关工具，按原样返回任务，不选择工具。\n"
        "- 如果工具未在可用工具列表中列出，不要建议使用该工具。\n"
    )

    context_template = "上下文: {context}\n {activated_tools}\n"

    template_answer = "任务: {tasks}\n"

    TOOL_ROUTING_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            SystemMessagePromptTemplate.from_template(context_template),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )

    custom_prompts[TemplatePromptName.TOOL_ROUTING_PROMPT] = TOOL_ROUTING_PROMPT

    system_message_zendesk_template = """
    You are a Customer Service Agent using Zendesk. You are answering a client query.
    You will be provided with the users metadata, ticket metadata and ticket history which can be used to answer the query.
    You will also have access to the most relevant similar tickets and additional information sometimes such as API calls.
    Never add something in brackets that needs to be filled like [your name], [your email], etc. 
    Do NOT invent information that was not present in previous tickets or in user metabadata or ticket metadata or additional information.
    Always prioritize information from the most recent tickets, especially if they are contradictory.
    
    Here is the current time: {current_time} UTC
    
    Here are default instructions that can be ignored if they are contradictory to the <instructions from me> section:
    <default instructions>
    - Don't be too verbose, use the same amount of details as in similar tickets.
    - Use the same tone, format, structure and lexical field as in similar tickets agent responses.
    - The text must be correctly formatted with paragraphs, bold, italic, etc so it is easier to read.
    - Maintain consistency in terminology used in recent tickets.
    - Answer in the same language as the user.
    - Don't add a signature at the end of the answer, it will be added once the answer is sent.
    </default instructions>
    
    
    Here are instructions that you MUST follow and prioritize over the <default instructions> section:
    <instructions from me>
    {guidelines}
    </instructions from me>
    """

    user_prompt_template = """
    Here is information about the user that can help you to answer:
    <user_metadata>
    {user_metadata}
    </user_metadata>

    Here are metadata on the current ticket that can help you to answer:
    <ticket_metadata>
    {ticket_metadata}
    </ticket_metadata>


    Here are the most relevant similar tickets that can help you to answer:
    <similar_tickets>
    {similar_tickets}
    </similar_tickets>

    Here are the current ticket history:
    <ticket_history>
    {ticket_history}
    </ticket_history>

    Here are additional information that can help you to answer:
    <additional_information>
    {additional_information}
    </additional_information>

    Here is the client question to which you must answer:
    <client_query>
    {client_query}
    </client_query>
 
    Based on the informations provided, answer directly with the message to send to the customer, ready to be sent:
    Answer:"""

    ZENDESK_TEMPLATE_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_zendesk_template),
            HumanMessagePromptTemplate.from_template(user_prompt_template),
        ]
    )
    custom_prompts[TemplatePromptName.ZENDESK_TEMPLATE_PROMPT] = ZENDESK_TEMPLATE_PROMPT

    system_message_template = "{enforced_system_prompt}"

    template_answer = """
    <draft answer>
    {task}
    <draft answer>
    Stick closely to this draft answer. Assume that the draft answer informations are correct, and do not try to outsmart him/her.
    Respond directly with the message to send to the customer, ready to be sent:

    Answer:
    """
    ZENDESK_LLM_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )
    custom_prompts[TemplatePromptName.ZENDESK_LLM_PROMPT] = ZENDESK_LLM_PROMPT

    return custom_prompts


_templ_registry: dict[TemplatePromptName, BasePromptTemplate] = _define_custom_prompts()

custom_prompts = types.MappingProxyType(_templ_registry)
