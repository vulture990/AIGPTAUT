import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from nextcaptcha import NextCaptchaAPI

# Replace with your actual NextCaptcha API key
CLIENT_KEY = "next_50c84695df4198baf4ac2f55b56de02c27"

# Initialize the NextCaptcha API
api = NextCaptchaAPI(client_key=CLIENT_KEY)

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

    # Wait for the iframe to appear
    try:
        print("Waiting for the CAPTCHA iframe to load.")
        iframe = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='Verification challenge']"))
        )
        print("CAPTCHA iframe found, switching to it.")
        driver.switch_to.frame(iframe)

        # Extract the website_public_key from the HTML
        print("Extracting website_public_key...")
        website_public_key_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='FunCaptcha-Token']"))
        )
        website_public_key_full = website_public_key_element.get_attribute("value")
        print(f"Extracted full website_public_key: {website_public_key_full}")

        # Correctly isolate the public key using "pk="
        start_index = website_public_key_full.find("pk=")
        if start_index != -1:
            website_public_key = website_public_key_full[start_index + 3:].split('|')[0]
            print(f"Isolated website_public_key: {website_public_key}")
        else:
            raise ValueError("Public key not found in the extracted value")

        # Solve FunCaptcha using NextCaptcha API
        result = api.funcaptcha(website_public_key=website_public_key)

        if result["status"] == "ready":
            captcha_solution = result['solution']['token']
            print(f"FunCaptcha solved: {captcha_solution}")

            # Insert the solution into the correct field
            driver.execute_script("document.querySelector('input[name=\"fc-token\"]').value = arguments[0];", captcha_solution)

            # Print the HTML after solving CAPTCHA
            time.sleep(2)  # Small delay to ensure everything is loaded

        else:
            print(f"Failed to solve FunCaptcha: {result['error']}")

    except Exception as e:
        print(f"An error occurred during CAPTCHA handling: {e}")
        driver.save_screenshot('captcha_error.png')  # Take a screenshot for debugging

finally:
    driver.quit()
