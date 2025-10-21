#Objectives:
# 1- Create multiple Nodes that sequentially process and update different parts of the AgentState
# 2- Connect nodes together in a graph
# 3- Compile and invoke the graph to see the final output

from typing import Dict, TypedDict, List
from langgraph.graph import StateGraph

class Agentstate(TypedDict):
    name: str
    age: str
    final: str

def first_node(state:Agentstate) -> Agentstate:
    """ This is the first node of our sequence """
    state['final'] = f'Hello {state['name']}'

    return state

def second_node(state:Agentstate) -> Agentstate:
    """ This is the second node of our sequence """
    state['final'] += f', you are {state["age"]} years old!'

    return state

graph = StateGraph(Agentstate)
graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.set_finish_point("second_node")
app = graph.compile()


with open("sequential.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())
print("Graph image saved as sequential.png")

result = app.invoke({
    "name" : 'Random User',
    'age' : '30'
})

print(result)