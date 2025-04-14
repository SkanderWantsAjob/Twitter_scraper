from playwright.sync_api import sync_playwright
import json
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL=os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
ACCOUNT_USERNAME = os.getenv("ACCOUNT_USERNAME")
def scrape_tweets(username, max_count=10, email="", password="", account_username=""):
    tweets = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        if email and password:
            page.goto("https://twitter.com/login")
            page.fill('input[name="text"]', email)
            page.wait_for_timeout(2000)
            page.locator('button:has-text("Next")').click()
            page.fill('input[name="password"]', password)
            page.locator('button:has-text("Log in")').click()
            page.wait_for_timeout(1000)

        page.goto(f"https://twitter.com/{username}")
        page.wait_for_timeout(5000)

        while len(tweets) < max_count:
            articles = page.locator('article')
            for i in range(articles.count()):
                article = articles.nth(i)
                try:
                    handle = article.locator('span:has-text("@")').first.inner_text()
                    text = article.locator('div[lang]').inner_text(timeout=2000)
                except:
                    continue

                if handle.lower() == f"@{username.lower()}" and text not in tweets:
                    tweets.append(text)
                    print(f"Added: {text}")
                    if len(tweets) >= max_count:
                        break

            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(2000)

        browser.close()
    return tweets

if __name__ == "__main__":
    tweets = scrape_tweets("RealDonaldTrump", 5, EMAIL, PASSWORD, ACCOUNT_USERNAME)
    with open("tweets.json", "w") as f:
        json.dump(tweets, f, indent=2, ensure_ascii=False)
