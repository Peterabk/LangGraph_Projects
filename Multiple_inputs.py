#Objectives:
# 1- Understand and define the AgentState Struct
# 2- Create a processing node that performs operations on list data
# 3- Set up LanGraph that processes and outputs computed results
# 4- Compile and invoke a graph with multiple inputs

from typing import Dict, TypedDict, List
from langgraph.graph import StateGraph

class AgenState(TypedDict):
    values: List[int]
    name: str
    result: str

def process_values(state:AgenState) -> AgenState:
    # See how the state is updatiing
    print(state)
    """This function handles multiple different inputs"""
    state['result'] = f'Hello there {state['name']}, your sum is {sum(state['values'])}'
    print(state)

    return state


graph = StateGraph(AgenState)

graph.add_node("processor", process_values)

graph.set_entry_point("processor")
graph.set_finish_point("processor")

# Never forget to compile your graph
app = graph.compile()

result = app.invoke({
    "values": [1,2,3,4,5,6],
    "name": "Random User"
})
print(result)