from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class PortFolioState(TypedDict):
    amount_usd: float
    total_usd: float
    total_inr: float


my_object: PortFolioState = {
    "amount_usd": 100,
    "total_usd":100,
    "total_inr": 100
}

def calc_total(state: PortFolioState) -> float:
    state["total_usd"] = state["amount_usd"] * 1.08 
    return state

def convert_to_inr(state: PortFolioState) -> float:
    state["total_inr"] = state["total_usd"] * 85
    return state

builder = StateGraph(PortFolioState)

builder.add_node("calc_total_node", calc_total)
builder.add_node("convert_to_inr_node", convert_to_inr)

builder.add_edge(START, "calc_total_node")
builder.add_edge("calc_total_node", "convert_to_inr_node")
builder.add_edge("convert_to_inr_node", END)

graph = builder.compile()

with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())

print("Graph image saved as graph.png")

result = graph.invoke({"amount_usd": 100})

print("Final Portfolio State:", result)
