import os
from typing import Any

from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool
from agb import AGB
from agb.session_params import CreateSessionParams


class CodeInterpreterInput(BaseModel):
    """Input schema for the code interpreter tool."""

    code: str = Field(description="Python code to execute.")


class CodeInterpreterFunctionTool:
    """
    This class calls arbitrary code against a Python Jupyter notebook.
    It requires an AGB_API_KEY to create a sandbox.
    """

    tool_name: str = "code_interpreter"

    def __init__(self):
        # Instantiate the sandbox - this is a long lived object
        # that's pinging the cloud to keep the sandbox alive.
        if "AGB_API_KEY" not in os.environ:
            raise Exception(
                "Code Interpreter tool called while AGB_API_KEY environment variable is not set. "
            )
        self.agb = AGB()
        # Create session with custom image
        params = CreateSessionParams(image_id="agb-code-space-1")
        # Create sandbox
        self.sbx = self.agb.create(params).session

    def close(self):
        """Close the sandbox session."""
        self.agb.delete(self.sbx)

    def _execute_code(self, code: str) -> dict[str, Any]:
        """Execute Python code in the sandbox and return results."""
        print(f"***Code Interpreting...\n{code}\n====")
        execution = self.sbx.code.run_code(code, "python")
        # Convert results to json-serializable dicts for LangChain tool outputs.
        results = []
        for item in execution.results or []:
            entry = {}
            if hasattr(item, "png") and item.png:
                entry["png"] = item.png
            if hasattr(item, "text") and item.text:
                entry["text"] = item.text
            if hasattr(item, "html") and item.html:
                entry["html"] = item.html
            if hasattr(item, "json") and item.json:
                entry["json"] = item.json
            if hasattr(item, "data") and item.data:
                entry["data"] = item.data
            if hasattr(item, "mime_type") and item.mime_type:
                entry["mime_type"] = item.mime_type
            results.append(entry)
        return {
            "results": results,
            "stdout": execution.logs.stdout,
            "stderr": execution.logs.stderr,
            "error": execution.error_message,
        }

    def to_langchain_tool(self) -> StructuredTool:
        """Convert to a LangChain StructuredTool."""
        return StructuredTool.from_function(
            func=self._execute_code,
            name=self.tool_name,
            description=(
                "Execute python code in a Jupyter notebook cell and returns any rich data "
                "(eg charts), stdout, stderr, and error."
            ),
            args_schema=CodeInterpreterInput,
            return_direct=False,
        )
