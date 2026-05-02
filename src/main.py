import time
import random
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.charityextra.com/")

    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Live Campaigns").click()
    page.wait_for_timeout(2000)
    page.wait_for_selector("text = Crowdfunders")
    page.click("text = Crowdfunders")
    page.wait_for_timeout(2000)
    page.mouse.wheel(0, 300)
    
    for _ in range(1, random.randint(15, 20)):
        scrool_amount = random.randint(200, 600)
        page.mouse.wheel(0, scrool_amount)
        time.sleep(random.uniform(0.5, 2))
    page.wait_for_timeout(3000)
    html = page.content()
    with open("data/Crowdfunders.html", "w", encoding="utf-8") as f:
        f.write(html)
    page.close()