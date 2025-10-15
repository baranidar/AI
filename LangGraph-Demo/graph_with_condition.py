from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class PortFolioState(TypedDict):
    amount_usd: float
    total_usd: float
    target_currency: Literal["EUR", "INR"]
    total: float

def calc_total(state: PortFolioState) -> float:
    state["total"] = state["amount_usd"] * 1.08
    state["total_usd"] = state["total"]
    return state

def convert_to_inr(state: PortFolioState) -> float:
    state["total"] = state["total"] * 85
    return state

def convert_to_eur(state: PortFolioState) -> float:
    state["total"] = state["total"] * 0.9
    return state


def choose_conversion(state: PortFolioState) -> str:
    return state["target_currency"]

builder = StateGraph(PortFolioState)

builder.add_node("calc_total_node", calc_total)
builder.add_node("convert_to_inr_node", convert_to_inr)
builder.add_node("convert_to_eur_node", convert_to_eur)

builder.add_edge(START, "calc_total_node")
builder.add_conditional_edges("calc_total_node", choose_conversion, {
    "INR": "convert_to_inr_node",
    "EUR": "convert_to_eur_node"
})  
builder.add_edge(["convert_to_inr_node","convert_to_eur_node"], END)

graph = builder.compile()

with open("graph_with_condition.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())

print("Graph image saved as graph_with_condition.png")

result = graph.invoke({"amount_usd": 100, "target_currency": "EUR"})

print("Final Portfolio State:", result)