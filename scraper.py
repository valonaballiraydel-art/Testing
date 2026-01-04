import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_standings(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    # wait for JavaScript to load
    time.sleep(5)

    # Classes on SofaScore can be dynamic — use XPaths or data-* attributes
    rows = driver.find_elements(
        By.XPATH, "//div[contains(@class,'tableRow') or contains(@class,'standingsRow')]"
    )

    standings = []
    for row in rows:
        try:
            position = row.find_element(By.XPATH, ".//div[contains(@class,'position')]").text
            team = row.find_element(By.XPATH, ".//div[contains(@class,'teamName')]").text
            points = row.find_element(By.XPATH, ".//div[contains(@class,'points')]").text
        except Exception:
            continue

        standings.append({
            "position": position.strip(),
            "team": team.strip(),
            "points": points.strip()
        })

    driver.quit()
    return {
        "url": url,
        "standings": standings
    }
