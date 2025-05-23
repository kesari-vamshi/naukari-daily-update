import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import openai

# Load env variables
load_dotenv()
NAUKRI_EMAIL = os.getenv("NAUKRI_EMAIL")
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def generate_headline(role, years_exp):
    return f"DevOps Engineer with {years_exp} years of experience specializing in cloud infrastructure, automation, and CI/CD pipelines."

def enhance_headline(old_headline):
    try:
        print("Enhancing headline with GPT and DevOps keywords...")
        client = openai.OpenAI()  # Use OpenAI client properly

        response = client.chat.completions.create(
            model="gpt-4o",  # or "gpt-3.5-turbo" if you don't have GPT-4 access
            messages=[
                {"role": "system", "content": "You are a resume optimization expert."},
                {"role": "user", "content": (
                    f"Take this resume headline: '{old_headline}'. "
                    "Slightly improve the language, and include 2-3 trending keywords relevant to a DevOps Engineer, "
                    "such as Docker, Kubernetes, CI/CD, Terraform, AWS, Jenkins, etc. "
                    "Keep the headline natural, concise, and under 200 characters."
                )}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"GPT Error: {e}")
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

        # Enter email
        wait.until(EC.visibility_of_element_located((By.ID, "usernameField"))).send_keys(NAUKRI_EMAIL)
        time.sleep(10)

        # Enter password
        wait.until(EC.visibility_of_element_located((By.ID, "passwordField"))).send_keys(NAUKRI_PASSWORD)
        time.sleep(10)

        # Click login button
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Login']"))).click()
        print("Login submitted")
        time.sleep(10)

        # Handle potential "password compromised" popup
        try:
            alert_ok = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'OK')]")))
            alert_ok.click()
            print("Clicked 'OK' on password compromised popup")
            time.sleep(10)
        except Exception:
            # No popup, continue
            pass

        # Navigate to profile page directly
        driver.get("https://www.naukri.com/mnjuser/profile")
        print("Navigated to profile page")
        time.sleep(10)

        # Click on first required element
        xpath_1 = '/html/body/div[3]/div/div/span/div/div/div/div/div/div[2]/div[1]/div/div/ul/li[3]/span'
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_1))).click()
        print("Clicked first element")
        time.sleep(10)

        # Click on second element
        xpath_2 = '/html/body/div[3]/div/div/span/div/div/div/div/div/div[2]/div[2]/div[5]/div/div/div[1]/span[2]'
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_2))).click()
        print("Clicked second element")
        time.sleep(10)

        # Wait for textarea to appear and update resume headline
        textarea_xpath = '//*[@id="resumeHeadlineTxt"]'
        textarea = wait.until(EC.visibility_of_element_located((By.XPATH, textarea_xpath)))

        # Generate and enhance headline using GPT
        base_headline = generate_headline("DevOps Engineer", 2.8)
        print("Generated base headline:", base_headline)
        time.sleep(10)

        enhanced_headline = enhance_headline(base_headline)
        print("Enhanced headline:", enhanced_headline)
        time.sleep(10)

        textarea.clear()
        textarea.send_keys(enhanced_headline)
        print("Updated headline in textarea")
        time.sleep(10)

        # Click save button
        save_button_xpath = '/html/body/div[6]/div[8]/div[2]/form/div[3]/div/button'
        wait.until(EC.element_to_be_clickable((By.XPATH, save_button_xpath))).click()
        print("Clicked save button")
        time.sleep(10)

        print("Resume headline updated successfully!")

    except Exception as e:
        print("Error occurred:", e)
    finally:
        print("Closing browser in 5 seconds...")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    main()
