import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def sanitize(text):
    """Sanitize text for use in filenames."""
    return (
        text.replace(" ", "")
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "")
            .replace("?", "")
            .replace("|", "")
            .replace('"', "")
            .replace("'", "")
            .strip() or "Unknown"
    )


def scrape_linkedin_jobs(username, search_url):
    # Setup user directory
    user_dir = Path(f"data/users/{username}/scraped_jobs")
    os.makedirs(user_dir, exist_ok=True)

    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument('--user-data-dir=/tmp/chrome-bhim')  # Isolated Chrome session
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_experimental_option("detach", True)

    # Start ChromeDriver
    try:
        driver = webdriver.Chrome(service=Service(), options=chrome_options)
    except Exception as e:
        print(f"❌ ChromeDriver failed to launch: {e}")
        return

    driver.get(search_url)
    input("\n⚠️ Please log in to LinkedIn in the opened browser, then press ENTER here to continue...\n")

    # Wait and scroll to load job cards
    try:
        body = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        for _ in range(5):
            body.send_keys(Keys.END)
            time.sleep(2)
    except Exception as e:
        print(f"❌ Could not scroll page: {e}")
        driver.quit()
        return

    # Try common LinkedIn job card selectors
    job_selectors = ['.base-card', '.job-card-container', '.job-card-list__title']
    jobs = []
    for selector in job_selectors:
        jobs = driver.find_elements(By.CSS_SELECTOR, selector)
        if jobs:
            break

    print(f"\n🔍 Found {len(jobs)} job cards on the page")

    count = 0
    for job_card in jobs:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", job_card)
            time.sleep(1)

            try:
                title = job_card.find_element(By.CLASS_NAME, 'job-card-list__title').text.strip()
            except:
                title = "N/A"

            try:
                company = job_card.find_element(By.CLASS_NAME, 'job-card-container__company-name').text.strip()
            except:
                company = "N/A"

            try:
                location = job_card.find_element(By.CLASS_NAME, 'job-card-container__metadata-item').text.strip()
            except:
                location = "N/A"

            try:
                job_url = job_card.find_element(By.TAG_NAME, 'a').get_attribute('href')
            except:
                job_url = "N/A"

            desc = "(To be fetched manually later — not available in card view)"

            # Log the job info
            print(f"\n--- Job {count+1} ---")
            print(f"Title: {title}")
            print(f"Company: {company}")
            print(f"Location: {location}")
            print(f"URL: {job_url}")

            filename = f"job_{count+1}_{sanitize(company)}_{sanitize(title)}.txt"
            filepath = user_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Job Title: {title}\n")
                f.write(f"Company: {company}\n")
                f.write(f"Location: {location}\n")
                f.write(f"Job URL: {job_url}\n\n")
                f.write(desc)

            print(f"✅ Saved: {filename}")
            count += 1

        except Exception as e:
            print(f"⚠️ Failed to scrape a job: {e}")
            continue

    print(f"\n🎉 Finished scraping {count} jobs. Files saved in {user_dir}/")
    driver.quit()


if __name__ == "__main__":
    print("👋 Welcome to LinkedIn Job Scraper")
    username = input("Enter your username (e.g., BhimMishra): ").strip().replace(" ", "")
    url = input("Paste your LinkedIn job search URL here: ").strip()
    scrape_linkedin_jobs(username, url)