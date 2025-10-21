# Objectives:
# 1- Implement conditional logic to route the flow of data to different nodes
# 2- USe Start and End nodes to manage the flow of the graph
# 3- Design multiple nodes to perform different operations
# 4- Create router node to handle decision-making and control graph flow

from typing import Dict, TypedDict, List
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    operation: str
    number1: int
    number2: int
    finalNumber: int

def adder(state:AgentState) -> AgentState:
    """ This node adds two numbers """
    state['finalNumber'] = state['number1'] + state['number2']
    return state

def substractor(state:AgentState) -> AgentState:
    """ This node subtracts two numbers """
    state['finalNumber'] = state['number1'] - state['number2']
    return state

def decide_next_node(state:AgentState) -> AgentState:
    """ This node decides which node to do next """
    if state['operation'] == '+':
        return "addition_operation"
    
    elif state['operation'] == '-':
        return "subtraction_operation"
    
graph = StateGraph(AgentState)
graph.add_node("add_node", adder)
graph.add_node("substract_node", substractor)
graph.add_node("router_node", lambda state:state) # passthrough function (meaning the state remains the state as it was)

graph.add_edge(START, "router_node")

graph.add_conditional_edges(
    "router_node", 
    decide_next_node, 
    {
        "addition_operation": "add_node",
        "subtraction_operation": "substract_node"
    }
        )

graph.add_edge("add_node", END)
graph.add_edge("substract_node", END)

app = graph.compile()
with open("conditional.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())
print("Graph image saved as conditional.png")

result = app.invoke(
    {
        "operation": "+",
        "number1": 10,
        "number2": 5,
        "finalNumber": 0
    }
)

print(result)