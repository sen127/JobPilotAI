
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fill_application_form(driver, profile_data, resume_path, cover_letter_path):
    """
    Fills out the application form using the provided profile data and document paths.
    Currently supports basic Workday form fields as a starting point.

    Args:
        driver (WebDriver): The Selenium WebDriver instance
        profile_data (dict): User profile details
        resume_path (str): Path to the resume file to upload
        cover_letter_path (str): Path to the cover letter file to upload
    """
    try:
        print("🔄 Filling application form...")

        # Fill in basic text fields (Workday examples - may vary per job)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys(profile_data.get("first_name", ""))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "lastName"))).send_keys(profile_data.get("last_name", ""))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(profile_data.get("email", ""))

        # Upload resume and cover letter
        try:
            resume_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@type="file" and contains(@name, "resume")]')))
            resume_input.send_keys(resume_path)
        except:
            print("⚠️ Resume upload field not found.")

        try:
            cover_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@type="file" and contains(@name, "coverLetter")]')))
            cover_input.send_keys(cover_letter_path)
        except:
            print("⚠️ Cover letter upload field not found.")

        print("✅ Form fields filled successfully.")
    except Exception as e:
        print(f"❌ Error while filling application form: {e}")