import requests
import time

CLIENT_ID = "MOYN1022"
PASSWORD = "Jay@111102"
PIN = "2002"

BOT_TOKEN = "8278307917:AAGb64GpoqeKvH8vvukC6Gbfzf1LT2DEENQ"
CHAT_ID = "10316000897"

def telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def angel_login():
    otp_req = requests.post(
        "https://apiconnect.angelone.in/rest/auth/angelbroking/user/v1/otp",
        json={"clientcode": CLIENT_ID},
    ).json()
    print("OTP Requested:", otp_req)
    telegram("📩 OTP sent!")

    otp = input("Enter OTP: ")
    login = requests.post(
        "https://apiconnect.angelone.in/rest/auth/angelbroking/user/v1/loginByOTP",
        json={"clientcode": CLIENT_ID, "otp": otp, "mpin": PIN},
    ).json()
    print("Login Response:", login)

    access = login["data"]["jwtToken"]
    return access

def get_ltp(access_token):
    r = requests.post(
        "https://apiconnect.angelone.in/rest/secure/angelbroking/market/v1/quote/ltp",
        json={"exchange": "NSE", "tradingsymbol": "TCS", "symboltoken": "11536"},
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()
    return r["data"]["ltp"]

def run():
    telegram("🚀 BOT STARTED")
    access = angel_login()
    prev = None
    while True:
        try:
            price = get_ltp(access)
            if prev is not None:
                if price > prev:
                    telegram(f"BUY SIGNAL at {price}")
                elif price < prev:
                    telegram(f"SELL SIGNAL at {price}")
            print("Price:", price)
            prev = price
            time.sleep(5)
        except Exception as e:
            print("Error:", e)
            time.sleep(5)

if __name__ == "__main__":
    run()
