import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Öffne Gumroad...")
        await page.goto("https://app.gumroad.com/signup", wait_until="networkidle")
        await page.screenshot(path="/home/node/.openclaw/workspace/scripts/gumroad_1.png")
        print("Screenshot 1 gespeichert")
        
        # Fill signup form
        try:
            await page.fill('input[name="email"]', "clawy.studio@gmail.com")
            await page.fill('input[name="password"]', "hanmaq-kydsov-xumCu2")
            print("Felder ausgefüllt")
            await page.screenshot(path="/home/node/.openclaw/workspace/scripts/gumroad_2.png")
            
            # Submit
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(3000)
            await page.screenshot(path="/home/node/.openclaw/workspace/scripts/gumroad_3.png")
            print("Formular abgeschickt, URL:", page.url)
        except Exception as e:
            print("Fehler:", e)
            await page.screenshot(path="/home/node/.openclaw/workspace/scripts/gumroad_error.png")
        
        await browser.close()

asyncio.run(main())
