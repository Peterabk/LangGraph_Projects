# Objective:
# 1- Implement looping logic to route the flow of data back to the nodes
# 2- Create a single conditional edge to hande decision-making and control grap flow

import random
from typing import Dict, TypedDict, List
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int


def greeting_node(state:AgentState) -> AgentState:
    """ This node creates a greeting message """
    state['name'] = f'Hello there {state["name"]}'
    state['counter'] = 0
    return state

def number_generator(state:AgentState) -> AgentState:
    """ This node generates a list of numbers """
    state['number'].append(random.randint(0,10))
    state['counter'] += 1
    return state

def should_continue(state:AgentState) -> AgentState:
    """ Function to decide whether to continue looping or finish """
    if state['counter'] < 5:
        print(f"Eentering Loop : {state['counter']}")
        return "looping" # continue looping
    else:
        return "exit" # exit the loop
    

graph = StateGraph(AgentState)
graph.add_node("greeting_node", greeting_node)
graph.add_node("number_generator", number_generator)

graph.add_edge(START, "greeting_node")
graph.add_edge("greeting_node", "number_generator")
graph.add_conditional_edges(
    "number_generator",
    should_continue,
    {
        "looping": "number_generator",
        "exit": END
    }
)

app = graph.compile()

with open("looping.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())
print("Graph image saved as looping.png")

result = app.invoke({
    "name": "Random User",
    "number": [],
    "counter": 0
})

print(result)