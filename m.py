import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import requests
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

            # Capture cookies from the driver
            cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
            print(f"Captured cookies: {cookies}")

            # Extract the session token from the original request in the HTML
            token_element = driver.execute_script("return document.querySelector('input[name=\"fc-token\"]').value;")
            print(f"Extracted session token: {token_element}")

            # Prepare the payload for the request
            payload = {
                "token": token_element,
                "sid": "us-east-1",
                "render_type": "canvas",
                "lang": "",
                "isAudioGame": "false",
                "is_compatibility_mode": "false",
                "apiBreakerVersion": "green",
                "analytics_tier": "40",
                "fc-token": captcha_solution  # Add the solved captcha token here
            }

            # Convert the payload to a URL-encoded string (required for x-www-form-urlencoded content type)
            encoded_payload = "&".join([f"{key}={value}" for key, value in payload.items()])

            # Define the URL for the CAPTCHA verification
            url = "https://tcr9i.openai.com/fc/gfct/"

            # Headers to mimic the original request
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "User-Agent": driver.execute_script("return navigator.userAgent;"),
                "Referer": driver.current_url,
                "Origin": "https://chat.openai.com",  # Adjust as necessary
                "Accept-Language": driver.execute_script("return navigator.language;"),
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Host": "tcr9i.openai.com"  # Ensure this is accurate
            }



            # Send the POST request with the captcha solution
            response = requests.post(url, data=encoded_payload, headers=headers, cookies=cookies)

            # Check the response status
            if response.status_code == 200:
                print("Captcha solution successfully submitted!")
                print("Response:", response.text)
            else:
                print(f"Failed to submit captcha solution. Status code: {response.status_code}")
                print("Response:", response.text)

        else:
            print(f"Failed to solve FunCaptcha: {result['error']}")

    except Exception as e:
        print(f"An error occurred during CAPTCHA handling: {e}")
        driver.save_screenshot('captcha_error.png')  # Take a screenshot for debugging

finally:
    driver.quit()
