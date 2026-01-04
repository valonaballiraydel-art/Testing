from playwright.sync_api import sync_playwright

def scrape_standings(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--single-process"
            ]
        )

        page = browser.new_page(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        )

        # Go to tournament URL
        page.goto(url, timeout=60000)

        # Force FOOTBALL context to load
        page.wait_for_selector('a[href*="/football/"]', timeout=60000)

        # Give React time to finish rendering standings
        page.wait_for_timeout(6000)

        # Try to locate table rows (standings)
        rows = page.query_selector_all("div[role='row']")

        results = []

        for row in rows:
            try:
                text = row.inner_text().strip()
                if text and len(text) > 5:
                    results.append(text)
            except:
                continue

        browser.close()

        return {
            "status": "football_page_loaded",
            "rows_found": len(results),
            "sample_rows": results[:10]  # show only first 10 rows
        }
