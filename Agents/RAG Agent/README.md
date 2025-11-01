# RAG Agent - Document Retrieval Assistant

A sophisticated Retrieval-Augmented Generation (RAG) agent built with LangGraph that enables intelligent question-answering from PDF documents. This agent combines vector search capabilities with conversational AI to provide accurate, context-aware responses about ROS2 control interfaces and hardware documentation.

## 🎯 Overview

The RAG Agent demonstrates advanced LangGraph patterns including:
- **Document Processing**: PDF loading and text chunking
- **Vector Storage**: ChromaDB integration for semantic search
- **Tool Integration**: Custom retrieval tools with error handling
- **Conditional Routing**: Smart decision-making for tool usage
- **State Management**: Complex conversation state handling

## 🏗️ Architecture

```
User Query → LLM Agent → Should Continue? → Retriever Tool → Vector Search → Document Chunks → Response
     ↑                                                                                              ↓
     └─────────────────────────── Response Generation ←─────────────────────────────────────────┘
```

### Core Components

1. **LLM Agent** (`call_llm`): Processes user queries and decides when to use tools
2. **Retriever Tool** (`retriever_tool`): Searches the vector database for relevant content
3. **Action Executor** (`take_Action`): Handles tool execution and result processing
4. **Conditional Router** (`should_continue`): Determines workflow continuation

## 📋 Features

### Document Processing
- **PDF Loading**: Automatic PDF document ingestion
- **Text Chunking**: Intelligent document splitting with overlap
- **Vector Embedding**: OpenAI embeddings for semantic search
- **Persistent Storage**: ChromaDB vector database with collection management

### Intelligent Retrieval
- **Semantic Search**: Similarity-based document retrieval
- **Configurable Results**: Adjustable number of returned chunks (k=5)
- **Content Filtering**: Relevance-based result filtering
- **Error Handling**: Robust error management and logging

### Conversational Interface
- **Interactive Chat**: Continuous conversation loop
- **Context Awareness**: Maintains conversation history
- **Citation Support**: References specific document sections
- **Exit Commands**: Graceful session termination

## 🚀 Quick Start

### Prerequisites

1. **Environment Setup**
```bash
# Create .env file with your OpenAI API key
OPENAI_API_KEY=your_api_key_here
PDF_PATH=your_pdf_path_here
COLLECTION_NAME=your_collection_name_here
```

### Running the Agent

```bash
cd Agents
python RAG_Agent.py
```

### Example Interaction

```
==== RAG AGENT ====

what is your question? What is the ROS2 control interface?

[INFO] Retriever tool called with query: 'ROS2 control interface'
[INFO] Retrieved 5 documents from vector store
[INFO] Processing chunk 1, content length: 847
[INFO] Processing chunk 2, content length: 923
...

AI RESPONSE:
Based on the ROS2 control interface documentation, the ROS2 control interface is...
[Detailed response with citations from the document]
```

## 🔧 Configuration

### Vector Store Settings
```python
# Document chunking parameters
chunk_size = 1000        # Characters per chunk
chunk_overlap = 200      # Overlap between chunks

# Retrieval parameters
search_type = "similarity"
search_kwargs = {"k": 5}  # Number of chunks to retrieve
```

### Model Configuration
```python
# LLM settings
model = "gpt-4o"
temperature = 0          # Deterministic responses

# Embedding model
embedding_model = "text-embedding-3-small"
```

### Storage Configuration
```python
persist_directory = "./chroma_db"
collection_name = os.getenv("COLLECTION_NAME")
```

## 📁 File Structure

```
Agents/
├── README.md                    # This documentation
├── RAG_Agent.py                # Main agent implementation
├── RAG_Agent.png              # Graph visualization
└── chroma_db/                 # Vector database storage
    ├── chroma.sqlite3         # SQLite database
    └── [collection_data]/     # Vector embeddings
```

## 🛠️ Technical Implementation

### State Management
```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
```

### Tool Definition
```python
@tool
def retriever_tool(query: str) -> str:
    """Searches and returns information from the ROS2 control interface document"""
    # Vector search implementation
    # Error handling and logging
    # Result formatting
```

### Graph Construction
```python
graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever_agent", take_Action)

graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        True: "retriever_agent",
        False: END
    }
)
```

## 🔍 Troubleshooting

### Common Issues

1. **No Retrieval Results**
   - Check if PDF file exists at specified path
   - Verify vector database is populated
   - Ensure OpenAI API key is valid

2. **Tool Call Failures**
   - Verify `should_continue` function logic
   - Check tool parameter passing
   - Review error logs for specific issues

3. **Vector Store Issues**
   - Delete and recreate `chroma_db` directory
   - Verify PDF loading and chunking process
   - Check embedding model compatibility

### Debug Mode
Enable detailed logging by checking console output:
```
[INFO] Retriever tool called with query: 'your_query'
[INFO] Retrieved X documents from vector store
[INFO] Processing chunk 1, content length: XXX
```

## 📊 Performance Metrics

- **Document Processing**: ~1000 characters per chunk with 200-character overlap
- **Retrieval Speed**: Sub-second semantic search
- **Context Window**: Optimized for GPT-4o token limits
- **Accuracy**: Citation-based responses with source references

## 🔄 Workflow Details

1. **Initialization**
   - Load environment variables
   - Initialize OpenAI models
   - Load and process PDF document
   - Create/load vector database

2. **Query Processing**
   - User input → HumanMessage
   - LLM processes query with system prompt
   - Decides whether to use retrieval tool

3. **Document Retrieval**
   - Semantic search in vector database
   - Retrieve top-k relevant chunks
   - Format results with chunk numbers

4. **Response Generation**
   - Combine retrieved context with query
   - Generate comprehensive response
   - Include document citations

## 🎛️ Customization Options

### Modify Document Source
```python
pdf_path = "path/to/your/document.pdf"
```

### Adjust Retrieval Parameters
```python
retriever = Vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 10}  # Retrieve more chunks
)
```

### Custom System Prompt
```python
system_prompt = """
Your custom instructions for the AI assistant...
"""
```

## 📈 Future Enhancements

- Multi-document support
- Advanced chunking strategies
- Hybrid search (semantic + keyword)
- Response caching
- Multi-modal document support
- Custom embedding fine-tuning

## 🤝 Usage Tips

1. **Specific Queries**: More specific questions yield better results
2. **Technical Terms**: Use domain-specific terminology for better matching
3. **Context Building**: Build on previous questions in the conversation
4. **Citation Verification**: Always verify cited information from source documents

## 📄 Dependencies

- `langchain-core`: Message handling and tool integration
- `langchain-openai`: OpenAI model integration
- `langchain-chroma`: Vector database operations
- `langchain-community`: PDF document loading
- `langgraph`: Graph-based agent architecture

---

*This RAG Agent serves as a comprehensive example of document-based question answering using LangGraph's advanced patterns and vector retrieval capabilities.*
