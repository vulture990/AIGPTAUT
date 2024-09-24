import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import csv

# Function to handle chat prompt sending and retry logic
def process_row(driver, index, prompt):
    for attempt in range(3):  # Retry up to 3 times
        try:
            # Step 1: Refresh the page to start a new chat
            driver.get("https://chatgpt.com/?model=gpt-4")
            print(f"Attempt {attempt + 1}: Navigated to chat page for row {index + 1}.")
            time.sleep(5)  # Wait for the page to load

            # Step 2: Find the input field (contenteditable) and enter the prompt
            textarea = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
            )
            textarea.click()  # Click on the editable div to focus it
            textarea.send_keys(prompt)
            print(f"Entered prompt from row {index + 1}: {prompt}")

            # Step 3: Click the send button
            send_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Send prompt']"))
            )
            send_button.click()
            print(f"Sent the prompt for row {index + 1} on attempt {attempt + 1}.")

            # Step 4: Wait for the response
            time.sleep(20)  # Adjust as necessary for response time
            response_div = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-message-author-role='assistant']"))
            )
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
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
]
options.add_argument(f"user-agent={random.choice(user_agents)}")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(options=options, version_main=127)

try:
    # Open the login page
    driver.get("https://chatgpt.com/?model=gpt-4")
    print("Navigated to the login page.")
    
    time.sleep(random.uniform(2, 3))

    # Click the login button
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='login-button']"))
    )
    login_button.click()
    print("Clicked on the login button.")
    
    time.sleep(random.uniform(2, 3))

    # Enter email
    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input#email-input"))
    )
    email_input.send_keys("test@wordpath.com")
    print("Entered email address.")
    
    # Click the continue button after entering the email
    continue_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue')]"))
    )
    continue_button.click()
    print("Clicked on the Continue button.")

    time.sleep(random.uniform(2, 3))

    # Find the password input field and enter password
    password_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input#password"))
    )
    password_input.send_keys("i2fskL%tgV5m")
    print("Entered password.")
    
    # Check if the "Continue" button is clickable and enabled
    next_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(),'Continue')]"))
    )
    
    # Ensure button is enabled
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and not(@disabled)]"))
    )
    
    # Click the "Continue" button
    next_button.click()
    print("Clicked on the Continue button after entering the password.")
    
    # Wait for the CAPTCHA (if present) to be solved manually
    print("Please solve the CAPTCHA manually.")
    input("Press Enter after you've solved the CAPTCHA and been redirected...")
    
    # Switch back to the default content
    driver.switch_to.default_content()
    print("CAPTCHA solved and user redirected. Continuing execution...")

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
