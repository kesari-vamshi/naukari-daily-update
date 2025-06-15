import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
NAUKRI_EMAIL = os.getenv("NAUKRI_EMAIL")
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def generate_headline(role, years_exp):
    return f"{role} with {years_exp} years of experience specializing in cloud infrastructure, automation, and CI/CD pipelines."

def enhance_headline(old_headline):
    try:
        print("Enhancing headline with Gemini and DevOps keywords...")

        model = genai.GenerativeModel("gemini-1.5-flash")  # use supported model
        prompt = (
            f"Take this resume headline: '{old_headline}'. "
            "Give me 3 enhanced versions using trending DevOps keywords like Docker, Kubernetes, CI/CD, Terraform, AWS, Jenkins, etc. "
            "Return each as a separate bullet point, no commentary."
        )

        response = model.generate_content(prompt)
        text = response.text.strip()

        # Extract bullet points
        options = [line.lstrip("*-• ").strip() for line in text.split("\n") if line.strip().startswith(("*", "-", "•"))]

        if options:
            print("\nAuto-selected enhanced headline (option 1):", options[0])
            return options[0]
        else:
            print("❌ No bullet points found in response. Using original headline.")
            return old_headline

    except Exception as e:
        print(f"Gemini Error: {e}")
        return old_headline

def main():
    # Setup Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 20)

    try:
        # Open login page
        driver.get("https://www.naukri.com/nlogin/login?URL=//www.naukri.com/mnjuser/profile")
        print("Login page opened")
        time.sleep(10)

        # Enter credentials
        wait.until(EC.visibility_of_element_located((By.ID, "usernameField"))).send_keys(NAUKRI_EMAIL)
        time.sleep(5)
        wait.until(EC.visibility_of_element_located((By.ID, "passwordField"))).send_keys(NAUKRI_PASSWORD)
        time.sleep(5)

        # Login
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Login']"))).click()
        print("Login submitted")
        time.sleep(10)

        # Handle optional popup
        try:
            alert_ok = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'OK')]")))
            alert_ok.click()
            print("Clicked 'OK' on alert")
            time.sleep(5)
        except Exception:
            pass

        # Navigate to profile page
        driver.get("https://www.naukri.com/mnjuser/profile")
        print("Navigated to profile page")
        time.sleep(10)

        # Click to edit resume headline
        xpath_1 = '/html/body/div[3]/div/div/span/div/div/div/div/div/div[2]/div[1]/div/div/ul/li[3]/span'
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_1))).click()
        print("Clicked edit section")
        time.sleep(5)

        xpath_2 = '/html/body/div[3]/div/div/span/div/div/div/div/div/div[2]/div[2]/div[5]/div/div/div[1]/span[2]'
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_2))).click()
        print("Clicked pencil icon")
        time.sleep(5)

        # Update resume headline
        textarea_xpath = '//*[@id="resumeHeadlineTxt"]'
        textarea = wait.until(EC.visibility_of_element_located((By.XPATH, textarea_xpath)))

        base_headline = generate_headline("DevOps Engineer", 2.8)
        print("Generated base headline:", base_headline)
        time.sleep(5)

        enhanced_headline = enhance_headline(base_headline)
        time.sleep(5)

        textarea.clear()
        textarea.send_keys(enhanced_headline)
        print("Updated headline in textarea")
        time.sleep(5)

        # Save headline
        save_button_xpath = '/html/body/div[6]/div[8]/div[2]/form/div[3]/div/button'
        wait.until(EC.element_to_be_clickable((By.XPATH, save_button_xpath))).click()
        print("Saved updated headline")
        time.sleep(5)

        print("✅ Resume headline updated successfully!")

    except Exception as e:
        print("❌ Error occurred:", e)
    finally:
        print("Closing browser in 5 seconds...")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    main()
