# Objectives:
# 1- Define state structure with a list of HumanMessage objects
# 2- Initialize a GPT-4o model using LangChain's ChatOpenAI
# 3- Sendingand handling different types of messages
# 4- Building and compiling the graph of the Agent

from typing import Dict, TypedDict, List
from langgraph.graph import StateGraph, START, END

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv # To load environment variables from a .env file

load_dotenv()  # Load environment variables from .env file

class AgentState(TypedDict):
    messages: List[HumanMessage]

# This wrapper does not have any memory to it, so it will not have a chat history
# Each time you invoke it, you need to provide the full context of the conversation
llm = ChatOpenAI(model="gpt-4o")


def process(state: AgentState) -> AgentState:
    response = llm.invoke(state['messages'])
    print(f"Response from GPT-4o: {response.content}")
    return state


graph = StateGraph(AgentState)
graph.add_node("process_node", process)
graph.add_edge(START, "process_node")
graph.add_edge("process_node", END)

agent = graph.compile()

user_input = input("ENTER MESSAGE: ")

while user_input != "exit":
    agent.invoke({
    "messages": [HumanMessage(content=user_input)]
    })
    user_input = input("ENTER MESSAGE: ")
