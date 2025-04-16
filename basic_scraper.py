from playwright.sync_api import sync_playwright
import json
import os
from dotenv import load_dotenv
import argparse

load_dotenv()
EMAIL=os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
ACCOUNT_USERNAME = os.getenv("ACCOUNT_USERNAME")
def scrape_tweets(username="RealDonaldTrump", max_count=2, email="", password="", account_username="", tracing=False):
    tweets = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        if tracing:
            context = browser.new_context()
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
            page = context.new_page()
        else:
            page= browser.new_page()

        if email and password:
            page.goto("https://twitter.com/login")
            page.fill('input[name="text"]', email)
            page.wait_for_timeout(700)
            page.locator('button:has-text("Next")').click()

            # Handle "unusual login" scenario
            if page.locator('span:has-text("unusual login")'):
                print("Unusual login detected")
                page.fill('input[name="text"]', account_username)
                page.wait_for_timeout(1000)
                page.locator('button:has-text("Next")').click()

            page.fill('input[name="password"]', password)
            page.wait_for_timeout(1000)
            page.locator('button:has-text("Log in")').click()
            page.wait_for_timeout(1000)

        # Go to target user's profile
        page.goto(f"https://twitter.com/{username}")
        page.wait_for_timeout(1000)

        # Scroll and collect tweets
        while len(tweets) < max_count:
            articles = page.locator('article')
            for i in range(articles.count()):
                article = articles.nth(i)
                try:
                    handle = article.locator('span:has-text("@")').first.inner_text(timeout=100)
                    text = article.locator('div[lang]').inner_text(timeout=100)
                except:
                    continue

                # Filter only target user's tweets
                if handle.lower() == f"@{username.lower()}" and text not in tweets:
                    tweets.append(text)
                    print("one tweet added")
                    if len(tweets) >= max_count:
                        break

            # Scroll to load more tweets
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1000)
        if tracing:
            print("traced")
            context.tracing.stop(path="trace.zip")
        browser.close()
    return tweets

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="scrape twitter from a twitter profile")
    parser.add_argument("username", help="Twitter username to scrape tweets from")
    parser.add_argument("-n", "--max_count", type=int, default=10, help= "maximum number of tweets to scrape")
    parser.add_argument("-t", "--trace", action="store_true", help="enable tracing and save trace.zip")
    
    args=parser.parse_args()
    
    tweets = scrape_tweets(args.username, args.max_count, EMAIL, PASSWORD, ACCOUNT_USERNAME, True)
    
    # Save tweets to file
    with open("tweets.json", "w") as f:
        json.dump(tweets, f, indent=2)
    
    # Display results
    for i, tweet in enumerate(tweets):
        print(f"{i + 1}. {tweet}")
