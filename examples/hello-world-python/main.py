from agb import AGB
from agb.session_params import CreateSessionParams
from dotenv import load_dotenv

load_dotenv()
agb = AGB()

# Create session with custom image
params = CreateSessionParams(
    image_id="agb-code-space-1"
)
result = agb.create(params)
if not result.success:
    print(f"Session creation failed: {result.error_message}")
    exit(1)
session = result.session

# Use different modules

# Code execution
code_result = session.code.run("import os; print(os.getcwd())", "python")
print("Code output:", code_result.logs)

# Command execution
cmd_result = session.command.execute("ls -la")
print("Command output:", cmd_result.output)

# File operations
session.file.write("/tmp/test.txt", "Hello World!")
file_result = session.file.read("/tmp/test.txt")
print("File content:", file_result.content)

agb.delete(session)