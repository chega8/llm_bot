from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from src.dep.agent import get_tavily
from src.dep.llm import get_saiga_llm_llamacpp


class AgentSearch:
    def __init__(self):
        self.llm = get_saiga_llm_llamacpp()

        self.init_agent()

    def search(self, prompt) -> dict:
        response = self.agent_executor.invoke(
            {"messages": [HumanMessage(content=prompt)]}
        )
        return response["messages"][-1].content

    def init_agent(self):
        instructions = """You are an assistant."""
        base_prompt = hub.pull("langchain-ai/openai-functions-template")
        prompt = base_prompt.partial(instructions=instructions)

        tavily = get_tavily()
        tools = [tavily]

        self.agent_executor = create_react_agent(self.llm, tools)

        # agent = create_openai_functions_agent(self.llm, tools, prompt)
        # self.agent_executor = AgentExecutor(
        #     agent=agent,
        #     tools=tools,
        #     verbose=True,
        # )
