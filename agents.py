from langchain_groq.chat_models import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

# model setup
model = ChatGroq(model="llama-3.1-8b-instant", temperature=0)


class SimpleToolAgent:
    """Minimal ReAct-style agent: call LLM → execute tools → return final answer."""

    def __init__(self, llm, tools: list):
        self.llm = llm.bind_tools(tools)
        self.tools = {t.name: t for t in tools}

    def invoke(self, input: dict) -> dict:
        messages = input["messages"]

        for _ in range(5):  # max 5 tool-call rounds
            response = self.llm.invoke(messages)
            messages.append(response)

            # No tool calls → we have the final answer
            if not response.tool_calls:
                break

            # Execute every tool the model requested
            for tc in response.tool_calls:
                tool_fn = self.tools.get(tc["name"])
                if tool_fn:
                    result = tool_fn.invoke(tc["args"])
                else:
                    result = f"Tool '{tc['name']}' not found."
                messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))

        return {"messages": messages}


# First Agent
def build_search_agent():
    return SimpleToolAgent(llm=model, tools=[web_search])


# Second Agent
def build_reader_agent():
    return SimpleToolAgent(llm=model, tools=[scrape_url])


# Writer Chain
writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "you are an expert research writer. write clean, structured and insightful reports.",
        ),
        (
            "human",
            """Write a detailed research report on the topic below.
        Topic : {topic}
        
        Research Gathered:
        {research}
        
        Structure the report as:
        - Introduction
        - Key Findings (minimum 3 well-explained points)
        - Conclusion
        - Sources (list all urls found in the research)
        
        Be detailed factual and professional.
        """,
        ),
    ]
)

writer_chain = writer_prompt | model | StrOutputParser()

# Critic Chain
critic_prompt = ChatPromptTemplate.from_messages(
    [
        ('system', 'you are a sharp and constructive research critic. Be honest and specific.'),
        ('human', """
        Review the research report below and evaluate it strictly.
        
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
        
        """)
    ]
)

critic_chain = critic_prompt | model | StrOutputParser()