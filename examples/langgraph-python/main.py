import base64
import json
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from code_interpreter_tool import CodeInterpreterFunctionTool

load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]


def build_graph(tools):
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
    )
    llm_with_tools = llm.bind_tools(tools)

    def assistant(state: State):
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    graph = StateGraph(State)
    graph.add_node("assistant", assistant)
    graph.add_node("tools", ToolNode(tools))
    graph.set_entry_point("assistant")
    graph.add_conditional_edges("assistant", tools_condition)
    graph.add_edge("tools", "assistant")
    return graph.compile()


def extract_and_save_png(messages) -> bool:
    for msg in messages:
        content = getattr(msg, "content", None)
        if not content or not isinstance(content, str):
            continue
        try:
            payload = json.loads(content)
        except json.JSONDecodeError:
            continue
        for result in payload.get("results", []):
            if isinstance(result, dict) and result.get("png"):
                png_data = base64.b64decode(result["png"])
                filename = "chart.png"
                with open(filename, "wb") as f:
                    f.write(png_data)
                print(f"Saved chart to {filename}")
                return True
    return False


def main():
    code_interpreter = CodeInterpreterFunctionTool()
    tools = [code_interpreter.to_langchain_tool()]
    app = build_graph(tools)

    try:
        inputs = {"messages": [("user", "plot and show a Bezier curve")]}
        result = app.invoke(inputs)
    finally:
        code_interpreter.close()

    messages = result.get("messages", [])
    print(messages)
    extract_and_save_png(messages)


if __name__ == "__main__":
    main()
