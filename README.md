# LangGraph Learning Projects

A comprehensive collection of LangGraph implementations demonstrating various graph patterns, agent architectures, and AI-powered applications. This repository serves as a practical learning resource for understanding LangGraph's capabilities through hands-on examples.

## 🚀 Project Overview

This repository contains multiple LangGraph projects that showcase different graph patterns and AI agent implementations:

### 📊 Core Graph Patterns

#### 1. **Sequential Graph** (`Sequential_Graph.py`)
Demonstrates basic sequential node processing with state management.

```python
# Example: Processing user information sequentially
result = app.invoke({
    "name": 'Random User',
    'age': '30'
})
# Output: "Hello Random User, you are 30 years old!"
```

**Key Features:**
- Sequential node execution
- State updates across nodes
- Basic graph compilation and invocation

#### 2. **Conditional Graph** (`Conditional_Graph.py`)
Shows conditional routing based on state values using decision nodes.

```python
# Example: Mathematical operations based on operator
result = app.invoke({
    "operation": "+",
    "number1": 10,
    "number2": 5,
    "finalNumber": 0
})
# Routes to addition node, result: finalNumber = 15
```

**Key Features:**
- Conditional edge routing
- Router nodes for decision making
- START and END node usage

#### 3. **Looping Graph** (`Looping_Graph.py`)
Implements looping logic with conditional continuation.

```python
# Example: Generate 5 random numbers with counter
result = app.invoke({
    "name": "Random User",
    "number": [],
    "counter": 0
})
# Loops 5 times, generating random numbers each iteration
```

**Key Features:**
- Loop control with counters
- Dynamic state modification
- Conditional loop termination

#### 4. **Multiple Inputs Processing** (`Multiple_inputs.py`)
Handles complex state structures with multiple data types.

```python
# Example: Process list of values with user context
result = app.invoke({
    "values": [1,2,3,4,5,6],
    "name": "Random User"
})
# Output: "Hello there Random User, your sum is 21"
```

**Key Features:**
- Complex state management
- List processing
- Multiple input handling

### 🤖 AI Agent Implementations

#### 1. **ChatBot Agent** (`Agents/ChatBot.py`)
Interactive conversational AI with persistent conversation history.

```python
# Features:
- GPT-4o integration
- Conversation history management
- HumanMessage/AIMessage handling
- Automatic conversation logging to file
```

**Key Capabilities:**
- Real-time conversation with OpenAI GPT-4o
- Persistent conversation state
- Automatic conversation export

#### 2. **ReAct Agent** (`Agents/React Agent/React_Agent.py`)
Reasoning and Acting agent with mathematical tool capabilities.

```python
# Example query: "Add 4 + 4, Subtract 2, Multiply by 3, Divide by 2"
# Agent uses tools: add(4,4) → subtract(8,2) → multiply(6,3) → divide(18,2) = 9
```

**Available Tools:**
- Addition, Subtraction, Multiplication, Division
- Tool call chaining
- Step-by-step reasoning

#### 3. **Document Drafter** (`Agents/Drafter.py`)
Collaborative document creation and editing assistant.

```python
# Features:
- Document content management
- Real-time editing capabilities
- File saving functionality
- Interactive document modification
```

**Key Features:**
- Global document state management
- Update and save tools
- Interactive editing workflow
- Automatic file persistence

#### 4. **RAG Agent** (`Agents/RAG_Agent/`)
Advanced Retrieval-Augmented Generation agent for document-based question answering.

**Key Capabilities:**
- PDF document processing and vector storage
- Semantic search with ChromaDB
- Intelligent document retrieval
- Context-aware responses with citations

*For detailed documentation, setup instructions, and technical implementation details, see the README.md file in the `Agents/` folder.*

## 🛠️ Technical Stack

- **LangGraph**: Graph-based AI application framework
- **LangChain**: AI application development framework
- **OpenAI GPT-4o**: Large language model
- **Python**: Core programming language
- **dotenv**: Environment variable management

## 📋 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- `langgraph==0.6.8`
- `langchain-core==0.3.78`
- `langchain-openai==0.3.35`
- `openai==2.2.0`
- `python-dotenv==1.1.1`

## 🚦 Getting Started

1. **Clone the repository**
```bash
git clone <repository-url>
cd LangGraph_Projects
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

4. **Run any example**
```bash
python Sequential_Graph.py
python Agents/ChatBot.py
python Agents/React_Agent/React_Agent.py
```

## 📁 Project Structure

```
LangGraph_Projects/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── Sequential_Graph.py                # Basic sequential processing
├── Conditional_Graph.py               # Conditional routing example
├── Conditional_Grpah_exercise.py      # Extended conditional logic
├── Looping_Graph.py                   # Loop implementation
├── Greeting_node.py                   # Simple greeting node
├── Multiple_inputs.py                 # Multi-input processing
├── Agents/                            # AI Agent implementations
│   ├── ChatBot.py                     # Conversational AI
│   ├── Drafter.py                     # Document editing assistant
│   └── React Agent/
│       ├── React_Agent.py             # ReAct pattern agent
│       └── React_Agent.png            # Graph visualization
├── *.png                              # Graph visualizations
└── logging.txt                        # Conversation logs
```

## 🎯 Learning Objectives

Each project demonstrates specific LangGraph concepts:

- **Graph Construction**: Building and compiling state graphs
- **Node Implementation**: Creating processing functions
- **State Management**: Handling complex state structures
- **Conditional Logic**: Implementing decision-making flows
- **Tool Integration**: Adding external capabilities to agents
- **Message Handling**: Working with different message types
- **Agent Patterns**: Implementing common AI agent architectures

## 🔧 Graph Visualization

Most projects generate PNG visualizations of their graph structures using Mermaid diagrams. These help understand the flow and connections between nodes.

## 📝 Usage Examples

### Basic Graph Pattern
```python
from langgraph.graph import StateGraph
from typing import TypedDict

class State(TypedDict):
    data: str

def process_node(state: State) -> State:
    state['data'] = f"Processed: {state['data']}"
    return state

graph = StateGraph(State)
graph.add_node("processor", process_node)
graph.set_entry_point("processor")
graph.set_finish_point("processor")
app = graph.compile()

result = app.invoke({"data": "input"})
```

### Agent with Tools
```python
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

@tool
def my_tool(input: str) -> str:
    """Process input with custom logic"""
    return f"Processed: {input}"

tools = [my_tool]
model = ChatOpenAI().bind_tools(tools)
tool_node = ToolNode(tools)
```
