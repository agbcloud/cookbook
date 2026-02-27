from agb import AGB
from agb.session_params import CreateSessionParams
from dotenv import load_dotenv

load_dotenv()

agb = AGB()
create_result = agb.create(CreateSessionParams(image_id="agb-computer-use-ubuntu-2204"))
if not create_result.success:
    raise SystemExit(f"Session creation failed: {create_result.error_message}")

session = create_result.session

# Open text editor and type text
session.computer.app.start("gedit %U")
session.computer.keyboard.type("Hello from AGB!")
screen_capture_result = session.computer.screen.capture()
print("Screenshot URL:", screen_capture_result.data)

agb.delete(session)