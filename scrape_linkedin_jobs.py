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
import json
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup


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

    profile_path = Path(f"data/users/{username}/user_profile.json")
    if profile_path.exists():
        with open(profile_path, "r", encoding="utf-8") as pf:
            user_profile = json.load(pf)
        print(f"ℹ️ Loaded existing user profile from {profile_path}")
    else:
        user_profile = {
            "name": "Bhim Mishra",
            "email": "bhim@example.com",
            "phone": "1234567890",
            "location": "Montreal, Canada"
        }
        os.makedirs(profile_path.parent, exist_ok=True)
        with open(profile_path, "w", encoding="utf-8") as pf:
            json.dump(user_profile, pf, indent=4)
        print(f"ℹ️ Saved default user profile to {profile_path}")

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

    job_cards = driver.find_elements(By.CSS_SELECTOR, '.base-card')
    count = 0
    job_index = []

    # Insert logic to scroll to and click each job card before attempting to locate the apply button
    for job_card in job_cards:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", job_card)
            job_card.click()
            time.sleep(2)  # wait for job details to load

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-apply-button"))
            )
        except Exception as e:
            print(f"⚠️ Could not click and load job card: {e}")
            continue

    for i, job_card in enumerate(job_cards):
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", job_card)
            job_card.click()
            time.sleep(2)

            # Wait for job details panel to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-apply-button"))
            )

            # More robust apply button interaction with retries and multiple selectors
            apply_selectors = [
                ".jobs-apply-button",
                ".artdeco-button--primary",
                ".apply-button",
                "button[data-control-name='jobdetails_topcard_inapply']",
                "button[data-control-name='jobdetails_topcard_standardapply']"
            ]
            apply_button = None
            for selector in apply_selectors:
                try:
                    apply_button = driver.find_element(By.CSS_SELECTOR, selector)
                    if apply_button:
                        driver.execute_script("arguments[0].scrollIntoView(true);", apply_button)
                        apply_button.click()
                        time.sleep(5)
                        break
                except:
                    continue
            if not apply_button:
                print("⚠️ Could not find any apply button for job.")
                continue

            initial_tabs = driver.window_handles
            all_tabs = driver.window_handles
            if len(all_tabs) > 1:
                driver.switch_to.window(all_tabs[-1])
            else:
                print("⚠️ New tab did not open.")
                continue

            # Wait for the external job page to fully load
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except Exception as e:
                print(f"⚠️ External page did not load properly: {e}")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue

            # Try scraping info from external job site
            title, company, location = "N/A", "N/A", "N/A"
            desc = "Job description not available."
            try:
                title_tag = driver.find_element(By.TAG_NAME, 'title')
                title = title_tag.get_attribute("innerText").strip()

                h1s = [h.text.strip() for h in driver.find_elements(By.TAG_NAME, "h1") if h.text.strip()]
                h2s = [h.text.strip() for h in driver.find_elements(By.TAG_NAME, "h2") if h.text.strip()]
                h3s = [h.text.strip() for h in driver.find_elements(By.TAG_NAME, "h3") if h.text.strip()]
                ps = [p.text.strip() for p in driver.find_elements(By.TAG_NAME, "p") if p.text.strip()]

                if h1s:
                    title = h1s[0]
                if h2s:
                    company = h2s[0]
                if h3s:
                    location = h3s[0]

                # Use BeautifulSoup to fetch elements even if deeply nested
                page_html = driver.page_source
                soup = BeautifulSoup(page_html, 'html.parser')
                body_text = soup.get_text(separator="\n").strip()
                desc = body_text[:2000]  # truncate to avoid overload

            except Exception as e:
                print(f"⚠️ Could not scrape full details: {e}")

            job_url = driver.current_url
            timestamp = int(time.time())
            filename = f"job_{count+1}_{sanitize(company)}_{sanitize(title)}_{timestamp}.txt"
            filepath = user_dir / filename

            print(f"\n--- Job {count+1} ---")
            print(f"Title: {title}")
            print(f"Company: {company}")
            print(f"Location: {location}")
            print(f"URL: {job_url}")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Job Title: {title}\n")
                f.write(f"Company: {company}\n")
                f.write(f"Location: {location}\n")
                f.write(f"Job URL: {job_url}\n\n")
                f.write(desc)

            job_index.append({
                "title": title,
                "company": company,
                "location": location,
                "url": job_url,
                "file": str(filepath)
            })

            print(f"✅ Saved: {filename}")
            count += 1

            # Close the external tab and switch back
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(f"⚠️ Error processing job card {i+1}: {e}")
            if len(driver.window_handles) > 1:
                try:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                except:
                    pass
            continue

    # Save job index to JSON file
    index_path = user_dir / "scraped_index.json"
    with open(index_path, "w", encoding="utf-8") as jf:
        json.dump(job_index, jf, indent=4)
    print(f"\n📄 Saved job index to {index_path}")

    print(f"\n🎉 Finished scraping {count} jobs. Files saved in {user_dir}/")
    driver.quit()


if __name__ == "__main__":
    print("👋 Welcome to LinkedIn Job Scraper")
    username = input("Enter your username (e.g., BhimMishra): ").strip().replace(" ", "")
    url = input("Paste your LinkedIn job search URL here: ").strip()
    scrape_linkedin_jobs(username, url)