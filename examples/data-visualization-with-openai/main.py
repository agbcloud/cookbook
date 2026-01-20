import sys
import os
import json
import base64

from dotenv import load_dotenv
from agb import AGB
from agb.session_params import CreateSessionParams
from openai import OpenAI

load_dotenv()

agb = AGB()

# Create session with custom image
params = CreateSessionParams(image_id="agb-code-space-1")
result = agb.create(params)
# Create sandbox
sbx = agb.create(params).session

# Upload the dataset to the sandbox
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(script_dir, "./dataset.csv")
sandbox_file_path = "/tmp/dataset.csv"

with open(dataset_path, "r", encoding="utf-8") as f:
    dataset_path_in_sandbox = sbx.file_system.write_file(sandbox_file_path, f.read())


def run_ai_generated_code(ai_generated_code: str):
    print("Running the code in the sandbox....")
    execution = sbx.code.run_code(ai_generated_code, "python")
    print("Code execution finished!")

    # First let's check if the code ran successfully.
    if not execution.success:
        print("AI-generated code had an error.")
        print(execution.error_message)
        agb.delete(sbx)
        sys.exit(1)

    result_idx = 0
    for result in execution.results:
        if result.png:
            # Save the png to a file
            # The png is in base64 format.
            with open(f"chart-{result_idx}.png", "wb") as f:
                f.write(base64.b64decode(result.png))
            print(f"Chart saved to chart-{result_idx}.png")
            result_idx += 1
    agb.delete(sbx)


prompt = f"""
I have a CSV file about music. It has about 5k rows. It's saved in the sandbox at {sandbox_file_path}.
These are the columns:
- 'Artist': string, The name of the artist who performed the song.
- 'Title': string, The title of the song.
- 'Year': string, The year in which the song was released.
- 'Sales': float, The total sales figure for the song, like "36.503".
- 'Streams': float, The number of streams the song has received.
- 'Radio Plays': float, The number of times the song has been played on the radio.
- 'Rating': float,A numerical rating or score associated with the song.

Write Python code that creates the bar chart showing top10 Artists by Sales in descending order.
Do NOT print or explore the data. Just create the visualization directly.

CRITICAL: Your code MUST end with this exact line to display the plot:
display(plt.gcf())"""

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

print("Waiting for model response...")
response = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "run_python_code",
                "description": "Run Python code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The Python code to run",
                        }
                    },
                    "required": ["code"],
                },
            },
        }
    ],
)

# Handle the response
message = response.choices[0].message
if message.tool_calls:
    for tool_call in message.tool_calls:
        if tool_call.function.name == "run_python_code":
            args = json.loads(tool_call.function.arguments)
            code = args["code"]
            print("Will run following code in the sandbox", code)
            # Execute the code in the sandbox
            run_ai_generated_code(code)
