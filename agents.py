from langchain_groq.chat_models import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage, SystemMessage
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()


class SimpleToolAgent:
    """Minimal ReAct-style agent: call LLM → execute tools → return final answer."""

    def __init__(self, llm, tools: list):
        self.llm = llm.bind_tools(tools)
        self.tools = {t.name: t for t in tools}

    def invoke(self, input: dict) -> dict:
        tool_names = "\n".join(f"- {name}" for name in self.tools.keys())
        messages = [
            SystemMessage(content=(
                "You are a research assistant. "
                f"You can ONLY use the following tools:\n{tool_names}\n"
                "Never invent or call any other tool name."
            ))
        ] + input["messages"]

        for _ in range(5):
            response = self.llm.invoke(messages)
            messages.append(response)

            if not response.tool_calls:
                break

            for tc in response.tool_calls:
                tool_fn = self.tools.get(tc["name"])
                if tool_fn:
                    result = tool_fn.invoke(tc["args"])
                else:
                    result = f"Tool '{tc['name']}' not found."
                messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))

        # Guarantee a final AIMessage text response
        if not isinstance(messages[-1], AIMessage):
            final = self.llm.invoke(messages)
            messages.append(final)

        return {"messages": messages}


# ✅ Each agent gets its own fresh LLM instance — no shared bind_tools state
def build_search_agent():
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    return SimpleToolAgent(llm=llm, tools=[web_search])


def build_reader_agent():
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    return SimpleToolAgent(llm=llm, tools=[scrape_url])


# Writer Chain
_writer_model = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clean, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional.
"""),
])

writer_chain = writer_prompt | _writer_model | StrOutputParser()


# Critic Chain
_critic_model = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score : X/10

Strengths:
- ...
- ...

Areas to improve:
- ...
- ...

One line verdict:
- ...
"""),
])

critic_chain = critic_prompt | _critic_model | StrOutputParser()
