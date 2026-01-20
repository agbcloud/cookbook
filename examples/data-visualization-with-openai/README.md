# Data Visualization (OpenAI + AGB Sandbox)

This example generates visualization code with OpenAI, runs it inside an AGB sandbox, and saves the resulting charts as PNG files.

## What the script does

- Creates an AGB sandbox session using a specific image.
- Uploads `dataset.csv` to `/tmp/dataset.csv` inside the sandbox.
- Asks OpenAI Chat Completions to generate plotting code (top 10 artists by `Sales`, descending).
- Executes the generated Python code in the sandbox.
- Extracts PNG outputs and saves them.

## Setup
### Set up .env
1. Copy .env.example to .env
2. Get API key from [AGB API key](https://agb.ai/console/overview) and set the `AGB_API_KEY` environment variable
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

After the script finishes, chart images will be saved in the current directory.
