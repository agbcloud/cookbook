import asyncio
from agb import AGB
from agb.session_params import CreateSessionParams
from agb.modules.browser import BrowserOption
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

async def main() -> None:
    agb = AGB()
    create_result = agb.create(CreateSessionParams(image_id="agb-browser-use-1"))
    if not create_result.success:
        raise SystemExit(f"Session creation failed: {create_result.error_message}")

    session = create_result.session
    try:
        ok = await session.browser.initialize_async(BrowserOption())
        if not ok:
            raise SystemExit("Browser initialization failed")

        endpoint_url = session.browser.get_endpoint_url()
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(endpoint_url)
            page = await browser.new_page()
            await page.goto("https://agb.cloud")
            print("Title:", await page.title())
            await browser.close()
    finally:
        agb.delete(session)


if __name__ == "__main__":
    asyncio.run(main())