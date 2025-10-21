from typing import Dict, TypedDict, List
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    operation1 : str
    operation2 : str
    number1: int
    number2: int
    number3: int
    number4: int
    finalNumber1 : int
    finalNumber2 : int

def adder_one(state:AgentState) -> AgentState:
    """ This node adds two numbers """
    state['finalNumber1'] = state['number1'] + state['number2']
    return state

def adder_two(state:AgentState) -> AgentState:
    """ This node adds two numbers """
    state['finalNumber2'] = state['number3'] + state['number4']
    return state

def substractor_one(state:AgentState) -> AgentState:
    """ This node subtracts two numbers """
    state['finalNumber1'] = state['number1'] - state['number2']
    return state

def substractor_two(state:AgentState) -> AgentState:
    """ This node subtracts two numbers """
    state['finalNumber2'] = state['number3'] - state['number4']
    return state

def router_one(state:AgentState) -> AgentState:
    """ This node decides which node to do next """
    if state['operation1'] == '+':
        return "addition_operation_one"
    elif state['operation1'] == '-':
        return "subtraction_operation_one"
    
def router_two(state:AgentState) -> AgentState:
    """ This node decides which node to do next """
    if state['operation2'] == '+':
        return "addition_operation_two"
    elif state['operation2'] == '-':
        return "subtraction_operation_two"
    
graph = StateGraph(AgentState)
graph.add_node("add_node_one", adder_one)
graph.add_node("add_node_two", adder_two)
graph.add_node("substract_node_one", substractor_one)
graph.add_node("substract_node_two", substractor_two)
graph.add_node("router_node_one", lambda state:state)
graph.add_node("router_node_two", lambda state:state)

graph.add_edge(START, "router_node_one")
graph.add_conditional_edges(
    "router_node_one",
    router_one,
    {
        "addition_operation_one": "add_node_one",
        "subtraction_operation_one": "substract_node_one" 
    }
)

graph.add_edge("add_node_one", "router_node_two")
graph.add_edge("substract_node_one", "router_node_two")
graph.add_conditional_edges(
    "router_node_two",
    router_two,
    {
        "addition_operation_two": "add_node_two",
        "subtraction_operation_two": "substract_node_two" 
    }
)
graph.add_edge("add_node_two", END)
graph.add_edge("substract_node_two", END)

app = graph.compile()

result = app.invoke({
    "operation1": "-",
    "operation2": "+",
    "number1": 10,
    "number2": 5,
    "number3": 7,
    "number4": 4,
    "finalNumber1": 0,
    "finalNumber2": 0
})

print(result)