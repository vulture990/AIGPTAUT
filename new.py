import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Initialize the ChromeDriver with options
options = uc.ChromeOptions()
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
]
options.add_argument(f"user-agent={random.choice(user_agents)}")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(options=options, version_main=127)

try:
    driver.get("https://chat.openai.com/")
    print("Navigated to the login page.")
    
    time.sleep(random.uniform(2, 5))

    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='login-button']"))
    )
    login_button.click()
    print("Clicked on the login button.")

    time.sleep(random.uniform(2, 5))

    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input#email-input"))
    )
    email_input.send_keys("test@wordpath.com")
    print("Entered email address.")

    continue_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue')]"))
    )
    continue_button.click()
    print("Clicked on the Continue button.")

    time.sleep(random.uniform(2, 5))

    password_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
    )
    password_input.send_keys("i2fskL%tgV5m")
    print("Entered password.")

    next_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue')]"))
    )
    next_button.click()
    print("Clicked on the Continue button after entering the password.")

    # Wait for the CAPTCHA iframe to appear and switch to it
    try:
        print("Waiting for the CAPTCHA iframe to load.")
        iframe = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='Verification challenge']"))
        )
        print("CAPTCHA iframe found, switching to it.")
        driver.switch_to.frame(iframe)

        # Allow user to manually solve the CAPTCHA
        print("Please solve the CAPTCHA manually.")
        
        # Wait for user to complete CAPTCHA and press Enter
        input("Press Enter after you've solved the CAPTCHA manually...")

        # After CAPTCHA is solved, switch back to the default content
        driver.switch_to.default_content()

        time.sleep(5)

        # Capture cookies from the driver
        cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
        print(f"Captured cookies: {cookies}")

        # # Optionally, extract any required tokens or data from the new page
        # try:
        #     token_element = driver.execute_script("return document.querySelector('input[name=\"fc-token\"]').value;")
        #     print(f"Extracted session token: {token_element}")
        # except Exception as e:
        #     print("Session token not found on the new page, skipping extraction.")

    except Exception as e:
        print(f"An error occurred during CAPTCHA handling: {e}")
        driver.save_screenshot('captcha_error.png')  # Take a screenshot for debugging

finally:
    driver.quit()
