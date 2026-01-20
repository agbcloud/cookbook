import base64
import json

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from code_interpreter_tool import CodeInterpreterFunctionTool

load_dotenv()

def main():
    # 1. Pick your favorite llm
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
    )

    # 2. Initialize the code interpreter tool
    code_interpreter = CodeInterpreterFunctionTool()
    code_interpreter_tool = code_interpreter.to_langchain_tool()
    tools = [code_interpreter_tool]

    # 3. Create agent using the new LangChain 1.x API
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a helpful assistant that can execute Python code.",
    )

    # 4. Invoke the agent
    inputs = {"messages": [{"role": "user", "content": "plot and show a Bezier curve"}]}
    result = agent.invoke(inputs)

    code_interpreter.close()

    # 5. Extract results from messages
    # The result contains a 'messages' list with all conversation messages
    messages = result.get("messages", [])
    print(messages)
    # Find tool messages that contain results
    for msg in messages:
        payload = None
        if hasattr(msg, "content") and msg.content:
            if isinstance(msg.content, str):
                try:
                    payload = json.loads(msg.content)
                    for r in payload["results"]:
                        if isinstance(r, dict) and r.get("png"):
                            # Decode the base64 encoded PNG data
                            png_data = base64.b64decode(r["png"])
                            # Save the decoded PNG data to a file
                            filename = "chart.png"
                            with open(filename, "wb") as f:
                                f.write(png_data)
                            print(f"Saved chart to {filename}")
                except:
                    payload = None

if __name__ == "__main__":
    main()
