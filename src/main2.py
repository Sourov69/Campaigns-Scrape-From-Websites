import time
import random
import re
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


# function for handling error in emplty page cases
def safe_text(tag, default=""):
    return tag.get_text(strip=True) if tag else default

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.charityextra.com/")
    page.wait_for_timeout(3000)

    page.get_by_role("button", name="Live Campaigns").click()
    page.wait_for_timeout(2000)

    page.wait_for_selector("text = Crowdfunders")
    page.click("text = Crowdfunders")

    page.wait_for_timeout(2000)
    page.mouse.wheel(0, 300)
    
    # scrolling campaign lists
    for _ in range(1, random.randint(7, 10)):
        scrool_amount = random.randint(200, 600)
        page.mouse.wheel(0, scrool_amount)
        time.sleep(random.uniform(0.5, 2))

    page.wait_for_timeout(3000)

    # all campaign navigating items
    items = page.locator("div.grid.grid-cols-1.md\:grid-cols-2.lg\:grid-cols-3.xl\:grid-cols-4.min-\[2000px\]\:grid-cols-4.gap-5.md\:gap-6.mx-auto.w-full.max-w-\[1400px\].transition-opacity.duration-200 > div")
    
    data = []
    for i in range(items.count()):
        with page.expect_navigation():
            items.nth(i).click()
            page.wait_for_timeout(2000)
            page.mouse.wheel(0, 400)
            page.wait_for_timeout(3000)
            html = page.content()

            soup = BeautifulSoup(html, 'html.parser')
            data.append({
                "campaign_name" : safe_text(soup.find("h5")),

                "target_amount" : safe_text(soup.select_one("div.raised-of-primary div.number-holder")),

                "amount_raised" : safe_text(soup.select_one("div.raised-figs")),

                "number_of_donors" : safe_text(soup.select_one("label#label-donors")),

                "emails_or_phone" : safe_text(soup.select_one("div.row.mid-donate.mt-3 > div"))        
                
            })
            print(len(data))
            page.go_back()
            page.wait_for_timeout(3000)

    df = pd.DataFrame(data)
    df.to_csv("scraped_data.csv", index=False)

    page.wait_for_timeout(3000)
    page.close()