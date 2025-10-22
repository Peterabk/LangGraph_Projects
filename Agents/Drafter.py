from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage # The foundational class for all message types in langGraph
from langchain_core.messages import ToolMessage # Passes data back to LLM after it calls a tool such as the content ..
from langchain_core.messages import SystemMessage, HumanMessage # Message for providing instructions to the LLM
from langchain_openai import ChatOpenAI # OpenAI chat model wrapper
from langchain_core.tools import tool # Tool decorator to create tools
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode

load_dotenv()  # Load environment variables from .env file


# This is the global variable to store document content
document_content = ""

class AgentState (TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Creating the tools
@tool
def update(content: str) -> str:
    """ Updates the document with the provided content """
    global document_content
    document_content = content
    return f"Document has been updated successfully. The current content is: \n{document_content}"

@tool
def save(filename: str) -> str:
    """ Save the current document to a text file and finish the process.

        Args:
            filename (str): The name of the file to save the document content to.
    """
    if not filename.endswith(".txt"):
        filename = f"{filename}.txt"

    try:
        with open(filename, "w") as file:
            file.write(document_content)
        print(f"Document saved successfully as {filename}.")
        return f"Document saved successfully as {filename}."
    except Exception as e:
        print(f"Failed to save document: {e}")
        return f"Failed to save document: {e}"
    
tools = [update, save]

model = ChatOpenAI(model= "gpt-4o").bind_tools(tools) # now gpt model has access to our tools

def our_agent(state:AgentState) -> AgentState:
    system_prompt = SystemMessage(content=f"""
            You are Drafter, a helpful writing assistant. You are going to help the user uupdate and modify documents.
            
            - If the user wants to update or modify content, use the "update" tool with the complete updated content.
            - If the user wants to save and finish, you need to use the "save" tool
            - Make sure to always show the current document state after modifications.
            
            the current document content is:
            {document_content} 
        """)
    
    if not state["messages"]:
        user_input = " I'm ready to help you update a document. What would you like to create?"
        user_message = HumanMessage(content=user_input)

    else:
        user_input = input("\nWhat would you like to do with the document?")
        print(f"\n USER: {user_input}")
        user_message = HumanMessage(content=user_input)

    all_messages = [system_prompt] + state["messages"] + [user_message]
    response = model.invoke(all_messages) # passing the system prompt and the state messages to the model

    print(f"\n AI: {response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"\n AI made a tool call: {[tc['name'] for tc in response.tool_calls]}")

    return {"messages": list(state["messages"]) + [user_message, response]} # updating the state message


def should_continue(state:AgentState) -> AgentState:
    """ Determine if we should continue or end the conversation"""
    messages = state["messages"]

    if not messages:
        return "continue"
    
    for message in reversed(messages):
        if (isinstance(message, ToolMessage) and
            "saved" in message.content.lower() and
            "document" in message.content.lower()):
            return "end" # End if the document has been saved
        
    return "continue"

def print_messages(messages):
    if not messages:
        return
    
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"\n TOOL RESULT: {message.content}")

graph = StateGraph(AgentState)

graph.add_node("agent", our_agent)
graph.add_node("tools", ToolNode(tools=tools))

graph.set_entry_point("agent")

graph.add_edge("agent", "tools")

graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue" : "agent",
        "end": END
    }
)

app = graph.compile()

def run_document_agent():
    print("\n ==== DRAFTER ====")

    state = {"messages": []}

    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])

    print("\n ==== SESSION ENDED ====")

if __name__ == "__main__":
    run_document_agent()
