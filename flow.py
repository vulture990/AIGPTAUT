import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
import csv

# Function to handle element waiting with retries
def wait_for_element(driver, by, value, retries=3, delay=5):
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"Attempt {attempt + 1}: Element {value} not found. Refreshing page.")
            driver.refresh()
            time.sleep(delay)
    raise Exception(f"Element with {by}='{value}' not found after {retries} retries.")

# Function to detect and handle Cloudflare challenge
def handle_cloudflare(driver):
    try:
        # Wait for Cloudflare challenge to complete (adjust the condition as needed)
        WebDriverWait(driver, 10).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'title'))
        )
        print("Cloudflare challenge completed.")
    except TimeoutException:
        print("No Cloudflare challenge detected.")

# Function to perform login
def login(driver):
    retries = 3
    for attempt in range(retries):
        try:
            # Open the login page
            driver.get("https://chatgpt.com")
            print("Navigated to the login page.")
            time.sleep(random.uniform(2, 3))

            # Handle Cloudflare challenge if present
            handle_cloudflare(driver)

            # Wait for the login button
            login_button = wait_for_element(driver, By.CSS_SELECTOR, "button[data-testid='login-button']")
            login_button.click()
            print("Clicked on the login button.")

            time.sleep(random.uniform(2, 3))

            # Enter email
            email_input = wait_for_element(driver, By.CSS_SELECTOR, "input#email-input")
            email_input.send_keys("test@wordpath.com")
            print("Entered email address.")

            # Click the continue button after entering the email
            continue_button = wait_for_element(driver, By.XPATH, "//button[contains(text(),'Continue')]")
            continue_button.click()
            print("Clicked on the Continue button.")

            time.sleep(random.uniform(2, 3))

            # Find the password input field and enter password
            password_input = wait_for_element(driver, By.CSS_SELECTOR, "input#password")
            password_input.send_keys("i2fskL%tgV5m")
            print("Entered password.")

            # Click the "Continue" button
            next_button = wait_for_element(driver, By.XPATH, "//button[@type='submit' and contains(text(),'Continue')]")
            next_button.click()
            print("Clicked on the Continue button after entering the password.")

            # # Automatically wait for CAPTCHA to be solved and for the page to redirect
            # print("Waiting for CAPTCHA to be solved...")

            # # Wait until the page is redirected or a post-CAPTCHA element is detected
            # WebDriverWait(driver, 300).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='some-post-captcha-element']"))
            # )
            # print("CAPTCHA solved and user redirected. Continuing execution...")

            return True  # Login successful

        except Exception as e:
            print(f"Login attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print("Retrying login...")
                driver.delete_all_cookies()
                time.sleep(5)
            else:
                print("Failed to log in after multiple attempts.")
                return False

# Function to handle chat prompt sending and retry logic
def process_row(driver, index, prompt):
    for attempt in range(3):  # Retry up to 3 times
        try:
            # Step 1: Refresh the page to start a new chat
            driver.get("https://chatgpt.com/?model=gpt-4")
            print(f"Attempt {attempt + 1}: Navigated to chat page for row {index + 1}.")
            time.sleep(5)  # Wait for the page to load

            # Handle Cloudflare challenge if present
            handle_cloudflare(driver)

            # Step 2: Find the input field (contenteditable) and enter the prompt
            textarea = wait_for_element(driver, By.CSS_SELECTOR, "div[contenteditable='true']")
            textarea.click()  # Click on the editable div to focus it
            textarea.send_keys(prompt)
            print(f"Entered prompt from row {index + 1}: {prompt}")

            # Step 3: Click the send button
            send_button = wait_for_element(driver, By.CSS_SELECTOR, "button[aria-label='Send prompt']")
            send_button.click()
            print(f"Sent the prompt for row {index + 1} on attempt {attempt + 1}.")

            # Step 4: Wait for the response
            time.sleep(20)  # Adjust as necessary for response time
            response_div = wait_for_element(driver, By.CSS_SELECTOR, "div[data-message-author-role='assistant']")
            response = response_div.text
            print(f"Captured response for row {index + 1}: {response}")

            return response  # Return the response if successful

        except Exception as e:
            print(f"Error on attempt {attempt + 1} for row {index + 1}: {e}")
            if attempt == 2:  # If it fails after 3 tries
                print(f"Failed to process row {index + 1} after 3 attempts.")
                return None  # Return None if all attempts fail

# Initialize the ChromeDriver with options
options = uc.ChromeOptions()
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Chrome/70.0.3538.77 Safari/537.36 Edge/18.19582",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Chrome/79.0.3945.117 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    # You can add more user agents if you wish
]
options.add_argument(f"user-agent={random.choice(user_agents)}")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(options=options)

try:
    # Perform login
    if not login(driver):
        print("Exiting script due to login failure.")
        exit()

    # Process the CSV file
    with open('AUTO.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    outputs = []

    for index, row in enumerate(rows):
        prompt = row['PROMPT']

        # Retry 3 attempts before moving to the next row
        response = process_row(driver, index, prompt)

        if response:
            output = {"prompt": prompt, "output": response}
        else:
            output = {"prompt": prompt, "output": "No response after 3 attempts"}
        
        outputs.append(output)

        # Write after each row in case of an error
        with open('new_AUTO.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['prompt', 'output']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(outputs)

    print("Completed processing and saved the results in new_AUTO.csv.")

    # Wait for 20 seconds before quitting
    print("Waiting for 20 seconds before quitting...")
    time.sleep(20)

except Exception as e:
    # Print more detailed error messages
    print(f"An error occurred: {e}")

finally:
    driver.quit()
