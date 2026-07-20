import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time #only here for debbuging should not be on final code


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    pageIndex = 1
    page.goto(f"https://iba-world.com/cocktails/all-cocktails/page/{pageIndex}/")

    page.get_by_role("button", name="Yes").click() #bypass age verification


    cocktailList = page.locator("#content > div > div.elementor.elementor-110 > section.elementor-section.elementor-top-section.elementor-element.elementor-element-5de9ae6.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div > div > div > div > div > div.iba-cocktails-container > div")
    links = cocktailList.get_by_role("link").all()

    for link in links:
        url = link.get_attribute("href")
        p = context.new_page()
        p.goto(url)
        time.sleep(2)
        p.close()

with sync_playwright() as playwright:
    run(playwright)