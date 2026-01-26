# Browser Use Quick Start for Python
This example creates a browser-enabled AGB session, connects with Playwright over CDP, opens agb.cloud, and prints the page title.

## Setup
### Set up .env
1. Copy .env.example to .env
2. Get API key from [AGB API key](https://agb.cloud/console/overview)

### Run with uv
#### 1. Install dependencies: 
```
uv sync
```
#### 2. Start the example: 
```
uv run python main.py
```

