import requests
from nextcaptcha import NextCaptchaAPI

# Replace with your actual NextCaptcha API key
CLIENT_KEY = "next_50c84695df4198baf4ac2f55b56de02c27"

# Initialize the NextCaptcha API
api = NextCaptchaAPI(client_key=CLIENT_KEY)

# Define the website public key (extracted from the page)
website_public_key = "0A1D34FC-659D-4E23-B17B-694DCFCF6A6C"

# Solve the FunCaptcha using the NextCaptcha API
result = api.funcaptcha(website_public_key=website_public_key)

if result["status"] == "ready":
    captcha_solution = result['solution']['token']
    print(f"FunCaptcha solved: {captcha_solution}")

    # Prepare the payload to submit the solution
    payload = {
        "token": "56717eeb1917b1955.3773702105",  # Replace with the correct session token
        "sid": "eu-west-1",
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

    # Define the URL where the solution should be submitted
    url = "https://tcr9i.openai.com/fc/gfct/"

    # Headers to mimic the original request
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Referer": "https://tcr9i.openai.com/v2/2.9.0/enforcement.b3b1c9343f2ef3887d61d74272d6a3af.html"
    }

    # Use the cookies you collected from the browser
    cookies = {
        "oai-did": "a1746b15-1a6e-4d70-b064-4646acc79dbe",
        "_cfuvid": "efpHJgfeK_Ef1rz6eyrePP_1hgTbA8DPdQsU5q8hdVM-1724380200414-0.0.1.1-604800000",
        "ajs_anonymous_id": "fa81db6a-6a34-4c93-aa4d-b2c19c98d393",
        "timestamp": "172459300705834",
        "_ga": "GA1.1.312556483.1721937434",
        "_ga_8MYC5SEFJ1": "GS1.1.1721937434.1.0.1721937440.0.0.0",
        "_cfuvid": "2Tcy_EqLJ0qhYnviOGCTm_1P9sZBMu9.hAx5FSqz2z4-1717104076479-0.0.1.1-604800000",
        "cf_clearance": "nJW_TfZOaKx9bYoZBQqQV0Jlu52dX8eaf029VDhvIlA-1721937438-1.0.1.1-yEhPdsQovkkxw9cVaWu4Bxa4qzzJ2OPkDG0xor6SHU0zIuk3Hp822SDthERnmKXmCq12cp6JUfuf2Rabv4a1lA",
        "intercom-device-id-dgkjq2bp": "f18331ac-5395-46a9-889e-f46391a942b6"
    }

    # Send the POST request with the captcha solution and cookies
    response = requests.post(url, data=encoded_payload, headers=headers, cookies=cookies)

    # Check the response status
    if response.status_code == 200:
        print("Captcha solution successfully submitted!")
        print("Response:", response.text)
    else:
        print(f"Failed to submit captcha solution. Status code: {response.status_code}")
        print("Response:", response.text)
else:
    print(f"Failed to solve FunCaptcha: {result.get('error', 'Unknown error')}")
