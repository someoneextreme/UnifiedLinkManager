import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_bing_results(query, num_results=200):
    # Brave and ChromeDriver paths handled automatically by webdriver-manager
    BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

    options = Options()
    options.binary_location = BRAVE_PATH
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")

    # Use webdriver-manager to get the latest compatible chromedriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.bing.com")

    # Search the query
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(query + Keys.RETURN)
    except Exception as e:
        print(f"❌ Search failed: {e}")
        driver.quit()
        return []

    results = []
    seen_links = set()

    while len(results) < num_results:
        try:
            # Try to dismiss cookie/consent popup
            try:
                consent_btn = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.ID, "bnp_btn_accept"))
                )
                driver.execute_script("arguments[0].click();", consent_btn)
                time.sleep(1)
            except:
                pass  # No popup, continue

            # Get current results
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.b_algo"))
            )
            items = driver.find_elements(By.CSS_SELECTOR, "li.b_algo")

            for item in items:
                try:
                    link_elem = item.find_element(By.TAG_NAME, "a")
                    title_elem = item.find_element(By.TAG_NAME, "h2")
                    link = link_elem.get_attribute("href")
                    title = title_elem.text.strip()

                    if link and link not in seen_links:
                        results.append((title, link))
                        seen_links.add(link)

                    if len(results) >= num_results:
                        break
                except:
                    continue

            # Go to next page
            if len(results) < num_results:
                next_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.sb_pagN"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                driver.execute_script("arguments[0].click();", next_btn)
                time.sleep(2)
        except Exception as e:
            print(f"No more pages or failed to navigate: {e}")
            break

    driver.quit()
    return results[:num_results]

def main():
    print("Search Scraper (Brave Browser)")
    query = input(" Enter search term: ")
    num = int(input(" Number of results to scrape: "))

    results = get_bing_results(query, num)

    if results:
        save_path = r"C:\Users\someoneextreme\Desktop\bing_results_brave.txt"
        with open(save_path, "w", encoding="utf-8") as f:
            for i, (title, link) in enumerate(results, 1):
                f.write(f"{i}. {title}\n{link}\n\n")
        print(f"Saved {len(results)} results to: {save_path}")
    else:
        print("No results found or scraping failed.")

if __name__ == "__main__":
    main()
