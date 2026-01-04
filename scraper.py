from playwright.sync_api import sync_playwright

def scrape_standings(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000)
        page.wait_for_timeout(5000)

        rows = page.query_selector_all("div[data-testid='standings-row']")

        standings = []
        for row in rows:
            try:
                position = row.query_selector("div:nth-child(1)").inner_text()
                team = row.query_selector("a").inner_text()
                points = row.query_selector("div:last-child").inner_text()
            except:
                continue

            standings.append({
                "position": position.strip(),
                "team": team.strip(),
                "points": points.strip()
            })

        browser.close()
        return standings
