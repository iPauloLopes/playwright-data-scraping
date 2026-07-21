from playwright.sync_api import Playwright, sync_playwright
import json


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://iba-world.com/cocktails/all-cocktails/page/1/")
    #page.get_by_role("button", name="Yes").click() #bypass age verification (only needed if headless=False)

    results = []
    
    while True:

        print("Loading...")
        cocktailPage = page.locator("div.iba-cocktails-container > div")
        cocktailList = cocktailPage.get_by_role("link").all()

        for link in cocktailList:
            links = link.get_attribute("href")

            p = context.new_page()
            p.goto(links)

            name = p.locator(".hfe-page-title > h1").inner_text()
            recipe = p.locator(".elementor-shortcode > ul").first.inner_text()

            results.append({
                "name":name,
                "recipe":recipe.splitlines()
            })

            p.close()

        nextPageButton = page.locator(".iba-cocktails-pagination > a.next")

        # breaks the loop if theres no 'next page' button
        if nextPageButton.is_visible():
            nextPageButton.click()
        else:
            break

        page.wait_for_load_state()

    # extract data as json file
    with open("recipes.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        print("data extraction complete")


with sync_playwright() as playwright:
    run(playwright)