from typing import Annotated
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

class State(TypedDict):
    messages: Annotated[list[str], add_messages]

def chatbot(state: State) -> State:
    return {"messages": [llm_with_tools.invoke(state['messages'])]}

@tool
def get_stock_price(symbol: str) -> str:
    """Get the stock price for a given symbol."""
    # Placeholder for actual stock price retrieval logic
    return {"MSFT": 2000,
            "AAPL": 1500,
            "GOOGL": 2500,
            "AMZN": 3000,
            "TSLA": 1000,
            "META": 1800,
            "NFLX": 1200
            }.get(symbol, "0.0")

tools = [get_stock_price]

llm = init_chat_model("google_genai:gemini-2.0-flash")
llm_with_tools = llm.bind_tools(tools)

builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
#builder.add_edge("chatbot_node", END)

graph = builder.compile()

with open("graph_with_tool_call.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())

print("Graph image saved as graph_with_tool_call.png")

state = None
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    if state is None:
        state = {"messages": [{"role": "user", "content": user_input}]}
    else:
        state["messages"].append({"role": "user", "content": user_input})
    state = graph.invoke(state)
    bot_response = state["messages"][-1].content
    print(f"Bot: {bot_response}")