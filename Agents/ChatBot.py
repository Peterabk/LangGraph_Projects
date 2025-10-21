# Objectives:
# 1- Use different message types - HumanMessage and AIMessage
# 2- Maintain conversation history using both message types
# 3- USe GPT-4o model using LangChain's ChatOpenAI
# 4- Create a sophisticated conversation loop

from typing import Dict, TypedDict, List, Union
from langgraph.graph import StateGraph, START, END

from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv # To load environment variables from a .env file

load_dotenv()  # Load environment variables from .env file

class AgentState(TypedDict):
    # List can contain both HumanMessage and AIMessage
    messages: List[Union[HumanMessage, AIMessage]] 

llm = ChatOpenAI(model="gpt-4o")

def process(state: AgentState) -> AgentState:
    """This node will solve the request you input"""
    response = llm.invoke(state["messages"])

    state['messages'].append(AIMessage(content=response.content))
    print(f"Response from GPT-4o: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process_node", process)
graph.add_edge(START, "process_node")
graph.add_edge("process_node", END)

agent = graph.compile()

conversation_history = []

user_input = input("ENTER MESSAGE: ")

while user_input != "exit":

    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({
    "messages": [HumanMessage(content=user_input)]
    })
    conversation_history = result['messages']
    user_input = input("ENTER MESSAGE: ")

with open("logging.txt", "w") as f:
    f.write("Your Conversation History:\n")

    for message in conversation_history:
        if isinstance(message, HumanMessage):
            f.write(f"Human: {message.content}\n")

        elif isinstance(message,AIMessage):
            f.write(f"AI: {message.content}\n")

    f.write("End of conversation. \n")

print("Conversation saved to logging.txt")