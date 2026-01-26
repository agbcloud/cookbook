# LangGraph + Code Interpreter (Python)
This example wires a LangGraph agent to an AGB-backed code interpreter tool, runs Python code in a sandbox, and saves a chart image locally.

## What the script does
- Creates an AGB sandbox session and exposes it as a LangGraph tool.
- Builds a LangGraph graph with a ChatOpenAI model and a tool node.
- Invokes the graph to generate and execute Python code (Bezier curve plot).
- Extracts PNG results from tool output and saves `chart.png`.

## Setup
### Set up .env
1. Copy .env.example to .env
2. Get API key from [AGB API key](https://agb.cloud/console/overview) and set the `AGB_API_KEY` environment variable
3. Set the `OPENAI_API_KEY` environment variable

### Run with uv
#### 1. Install dependencies:
```
uv sync
```
#### 2. Start the example:
```
uv run python main.py
```

After the script finishes, `chart.png` will be saved in the current directory.
