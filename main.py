import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time #only here for debbuging should not be on final code


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    pageIndex = 1
    
    page.goto(f"https://iba-world.com/cocktails/all-cocktails/page/{pageIndex}/")

    page.get_by_role("button", name="Yes").click()
    
    time.sleep(5)
    browser.close()

with sync_playwright() as playwright:
    run(playwright)