import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import csv

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
    
    time.sleep(random.uniform(2, 3))

    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='login-button']"))
    )
    login_button.click()
    print("Clicked on the login button.")

    time.sleep(random.uniform(2, 3))

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

    time.sleep(random.uniform(2, 3))

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

    # Wait for the CAPTCHA to be solved manually
    print("Please solve the CAPTCHA manually.")
    input("Press Enter after you've solved the CAPTCHA and been redirected...")

    # Switch back to the default content
    driver.switch_to.default_content()
    print("CAPTCHA solved and user redirected. Continuing execution...")

    # Process the CSV
    with open('AUTO.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    outputs = []

    for row in rows:
        prompt = row['PROMPT']

        # Find the textarea and enter the prompt
        textarea = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea#prompt-textarea"))
        )
        textarea.send_keys(prompt)
        print(f"Entered prompt: {prompt}")

        # Click the send button
        send_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Send prompt']"))
        )
        send_button.click()
        print("Sent the prompt.")

        time.sleep(25)  # Increased wait time for response

        responses = []
        for i in range(4):  # Initial response + 3 regenerations
            # Locate the response container dynamically
            response_div = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-message-author-role='assistant']"))
            )
            response = response_div.text
            print(f"Captured response {i + 1}: {response}")
            responses.append(response)

            if i < 3:  # Don't regenerate after the last response
                regenerate_button = WebDriverWait(driver, 40).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Regenerate']"))
                )
                regenerate_button.click()
                print(f"Regenerated response {i + 1}")
                time.sleep(15)  # Increased wait time before capturing the next response

        # Save all responses in the 'output' list, separated by new lines
        outputs.append({"prompt": prompt, "output": "\n\n".join(responses)})

    # Write the new CSV with prompts and outputs
    with open('new_AUTO.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['prompt', 'output']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(outputs)

    print("Completed processing the CSV file and saved the results in new_AUTO.csv.")

    # Wait for 300 seconds before quitting
    print("Waiting for 300 seconds before quitting...")
    time.sleep(300)

except Exception as e:
    print(f"An error occurred during login or CSV processing: {e}")

finally:
    driver.quit()
