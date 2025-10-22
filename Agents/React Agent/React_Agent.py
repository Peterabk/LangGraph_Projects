# Objective:
# 1- learn how to create Rools in LangGraph
# 2- How to Create a React Graph
# 3- Work with different types of Messages such as ToolMessages
# 4- Test out robustness of our graph

# Main Goal: Create a robust React Agent!

from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage # The foundational class for all message types in langGraph
from langchain_core.messages import ToolMessage # Passes data back to LLM after it calls a tool such as the content ..
from langchain_core.messages import SystemMessage # Message for providing instructions to the LLM
from langchain_openai import ChatOpenAI # OpenAI chat model wrapper
from langchain_core.tools import tool # Tool decorator to create tools
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode

load_dotenv()  # Load environment variables from .env file

class AgentState (TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Creating the tool
@tool
def add(a: int, b: int ):
    """This is an addition function that adds 2 numbers together"""
    return a + b

@tool
def substract(a: int, b: int ):
    """This is a substraction function that substracts 2 numbers from eahch other"""
    return a - b

@tool
def multiply(a: int, b: int ):
    """This is a multiplication function that multiplies 2 numbers together"""
    return a * b

@tool
def divide(a: int, b: int ):
    """This is a division function that divides 2 numbers together"""
    return a / b

# tools list
tools = [add, substract, multiply, divide]

model = ChatOpenAI(model= "gpt-4o").bind_tools(tools) # now gpt model has access to our tools

def model_call(state:AgentState) -> AgentState:
    system_prompt = SystemMessage(content= "You are my AI assistant, please answer my query to the best of your ability")
    response = model.invoke([system_prompt] + state["messages"]) # passing the system prompt and the state messages to the model
    return {"messages": response} # updating the state message

def should_continue(state:AgentState) -> AgentState:
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:  # If there are no tool calls, we are done
        return "end"
    
    else:
        return "continue"
    
graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue" : "tools",
        "end": END
    }
)

graph.add_edge("tools", "our_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

# Create the image of the graph
# Save the image to a file instead of displaying it
with open("React_Agent.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())
print("Graph image saved as React_Agent.png")

inputs = {
    "messages": [
        ("user", "Add 4 + 4, Substract the result by 2, Multiply the result by 3, Divide by 2, What is the final result?" )
    ]
}
#"Add 40 + 12 and then multiply the result by 6. Also tell me a joke please"

print_stream(app.stream(inputs, stream_mode="values"))