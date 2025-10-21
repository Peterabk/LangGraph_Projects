# Objectives:
# 1- Understand and define the AgentState Struct
# 2- Create simple node functions
# 3- Set up basic LangGraph struct
# 4- Compile and invoke a graph
# 5- Understand how data flow through a single-node


from typing import Dict, TypedDict
from langgraph.graph import StateGraph

# Optional: to visualize the graph
from IPython.display import Image, display

# we now create an AgentState - shared data strcutre that keeps track of information as your application runs
# State Schema
class AgentState(TypedDict):
    message : str

# Creating our first node
# We want to create a greeting message
def greeting_message(state: AgentState) -> AgentState:
    state["message"] = f"Hello World!, Hello {state['message']}"

    return state

# Now we build the graph
graph = StateGraph(AgentState)

# To add a node, you need the name of the node and the function that it will execute
graph.add_node("greeter", greeting_message)

graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app = graph.compile()

# Create the image of the graph
# Save the image to a file instead of displaying it
with open("greeting.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())
print("Graph image saved as greeting.png")

# If you are in a Jupyter environment, you can display the graph like this:
#display(Image(app.get_graph().draw_mermaid_png()))

# To run the appliocation
result = app.invoke({"message": "Generic Name"})
print(result)