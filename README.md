# Twitter Scraper (Playwright + Python)

A simple Python script that scrapes tweets from a public Twitter profile using Playwright. Optionally, it can log in (with a dummy account), scroll through the timeline, and collect a specified number of tweets. The result is saved as a JSON file.

By default, the script uses Donald Trump’s Twitter account since his tweets are varied and provide good test data.

---

## Features

- Scrapes tweets from any public profile.
- Can log in with a dummy account to bypass certain limitations.
- Optional Playwright tracing (saves `trace.zip`).
- Outputs scraped tweets in a `tweets.json` file.
- Command-line interface for easy usage.

---

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt

Then install the Playwright browser binaries:

```
playwright install
```

## .env Setup

Create a `.env` file in the root directory with the following keys:

```
EMAIL=your_dummy_email@example.com
PASSWORD=your_dummy_password
ACCOUNT_USERNAME=your_dummy_handle
```

## Usage

Run the script by specifying the Twitter username and number of tweets to scrape:

```
python basic_scraper.py username_here -n 5
```

### Optional flags:

- `-n`, `--max_count`: Number of tweets to scrape (default: 10)
- `-t`, `--trace`: Enable tracing and generate `trace.zip`

### Example with tracing:

```
python basic_scraper.py RealDonaldTrump -n 20 -t
```

## Output

The scraped tweets will be saved to a `tweets.json` file.
