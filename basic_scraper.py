from playwright.sync_api import sync_playwright
import json

def scrape_tweets(username, max_count=10):
    tweets = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(f"https://twitter.com/{username}")
        page.wait_for_timeout(5000)

        while len(tweets) < max_count:
            articles = page.locator('article')
            for i in range(articles.count()):
                article = articles.nth(i)
                try:
                    text = article.locator('div[lang]').inner_text(timeout=2000)
                except:
                    continue

                if text not in tweets:
                    tweets.append(text)
                    print(f"Added: {text}")
                    if len(tweets) >= max_count:
                        break

            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(2000)

        browser.close()
    return tweets

if __name__ == "__main__":
    tweets = scrape_tweets("RealDonaldTrump", 5)
    with open("tweets.json", "w") as f:
        json.dump(tweets, f, indent=2, ensure_ascii=False)
