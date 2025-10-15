from typing import Annotated
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

load_dotenv()

llm = init_chat_model("google_genai:gemini-2.0-flash")
# result = llm.invoke(
#     "What is the capital of France?",
#     stream=True
# )

# print(result) 

class State(TypedDict):
    messages: Annotated[list[str], add_messages]

def chatbot(state: State) -> State:
    return {"messages": [llm.invoke(state['messages'])]}

builder = StateGraph(State)
builder.add_node("chatbot_node", chatbot)
builder.add_edge(START, "chatbot_node")
builder.add_edge("chatbot_node", END)

graph = builder.compile()

# messages = {"role": "user", "content":"What is the capital of France?"}

# response = graph.invoke({"messages": [messages]})

# print(response["messages"])

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