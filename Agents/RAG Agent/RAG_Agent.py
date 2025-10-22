import os
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
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma

#Import not working, why?
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()  # Load environment variables from .env file

llm = ChatOpenAI(model= "gpt-4o", temperature=0) # to minimize hallucination and ensure deterministic responses

#Our Embedding Model - has to also be compatible with the LLM
embeddings = OpenAIEmbeddings(model= "text-embedding-3-small")

pdf_path = os.getenv("PDF_PATH")

#safety measure
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"The specified PDF file was not found: {pdf_path}")

pdf_loader = PyPDFLoader(pdf_path)

# Checks if the PDF has any pages
try:
    pages = pdf_loader.load()
    print(f"Loaded {len(pages)} pages from the PDF.")
except Exception as e:
    print(f"Error loading PDF: {e}")
    raise

# Chunking Process
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

pages_split = text_splitter.split_documents(pages) # we now apply this to our pages

persist_directory = r"./Agents/chroma_db"
collection_name = os.getenv("COLLECTION_NAME")

# If our collection does not exist in the directory, we create using the os
if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)

try:
    # Here, we actually create the chroma database using our embeddings model
    Vectorstore = Chroma.from_documents(
        documents=pages_split,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    print(f"Created ChromaDB vectore store!")

except Exception as e:
    print(f"Error creating ChromaDB: {e}")
    raise


# Now we create our retriever
retriever = Vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k":5}  # K is the amount of chunks to return
)

@tool
def retriever_tool(query: str) -> str:
    """ This tool searches and returns the information from the Ros2 control interface document """
    
    print(f"[INFO] Retriever tool called with query: '{query}'")
    
    try:
        docs = retriever.invoke(query)
        print(f"[INFO] Retrieved {len(docs)} documents from vector store")
        
        if not docs:
            print("[WARNING] No documents retrieved from vector store")
            return "No relevant information found in the document."
        
        results = []
        for i, doc in enumerate(docs):
            print(f"[INFO] Processing chunk {i+1}, content length: {len(doc.page_content)}")
            results.append(f"Chunk {i+1}:\n{doc.page_content}\n")

        final_result = "\n\n".join(results)
        print(f"[INFO] Returning combined result with {len(final_result)} characters")
        return final_result
        
    except Exception as e:
        print(f"[ERROR] Error in retriever_tool: {e}")
        return f"Error retrieving information: {str(e)}"

tools = [retriever_tool]

llm = llm.bind_tools(tools) # now gpt model has access to our tools

class AgentState (TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def should_continue(state:AgentState) -> bool:
    """Check if the last message contains tool calls"""
    last_message = state["messages"][-1]
    return hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0

system_prompt = """
You are an AI assistant who answers questions about Ros2 and Ros2 control interfaces.
Use the retriever tool available to answer questions aabout the ros2 control interface and hardware.
If you need to look up some information before asking a follow up question, you are allowed to do that.
please always cite the specific parts of the documents you use in your answers.
"""

tools_dict = {our_tool.name: our_tool for our_tool in tools} # Creating a dictionary of our tools

#LLM Agent
def call_llm(state:AgentState) -> AgentState:
    """Function to call the LLM with the current state"""
    messages = list(state["messages"])
    messages = [SystemMessage(content=system_prompt)] + messages
    message = llm.invoke(messages) # passing the system prompt and the state messages to the model
    return {"messages": [message]} # updating the state message

#Retriever Agent
def take_Action(state:AgentState) -> AgentState:
    """Execute tool calls from the LLM's response"""

    tool_calls = state["messages"][-1].tool_calls  # Get tool calls from the last message
    results = []
    for t in tool_calls:
        print(f"Calling tool: {t['name']} with query: {t['args'].get('query', 'No query provided')}")

        if not t["name"] in tools_dict:
            print(f"\nTool: {t['name']} not found!")
            result = " Incorrect Tool Name, Please Retry and Select tool from List of Available tools"

        else:
            print(f"Invoking tool with args: {t['args']}")
            result = tools_dict[t['name']].invoke(t['args'])
            print(f"Result length: {len(str(result))}")
            print(f"Retrieved content preview: {str(result)[:200]}...")

        # Appends the Tool Message
        results.append(ToolMessage(
            tool_call_id=t['id'],
            name=t['name'],
            content=str(result)))

        
    print("Tools Execution Complete. Back to the model.")
    return {"messages": results}  # Return the tool messages as the new state

graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever_agent", take_Action)

graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        True : "retriever_agent",
        False: END
    }
)

graph.add_edge("retriever_agent", "llm")
graph.set_entry_point("llm")

app = graph.compile()

# Create the image of the graph
# Save the image to a file instead of displaying it
with open("RAG_Agent.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())
print("Graph image saved as RAG_Agent.png")

def running_agent():
    print("\n ==== RAG AGENT ====")

    while True:
        user_input = input("\n what is your question?")
        if user_input.lower() in ["exit", "quit"]:
            break

        messages = [HumanMessage(content=user_input)] # Converts back to HumanMessage
        result = app.invoke({"messages": messages})
        final_message = result["messages"][-1].content
        print("\n AI RESPONSE:")
        print(final_message)

running_agent()