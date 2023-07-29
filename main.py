from bs4 import BeautifulSoup
import requests
import lxml
import smtplib
import os
import time

class AmazonPriceChecker:
    MY_EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("GMAIL_PASSWORD")

    def __init__(self):
        self.BASE_URL = "https://www.amazon.com/dp/B08THS5LM6/ref=sspa_dk_detail_3?psc=1&pd_rd_i=B08THS5LM6&pd_rd_w=9mGEy&content-id=amzn1.sym.0d1092dc-81bb-493f-8769-d5c802257e94&pf_rd_p=0d1092dc-81bb-493f-8769-d5c802257e94&pf_rd_r=23XABC324QFYZ75S82SE&pd_rd_wg=Q9xiQ&pd_rd_r=cf4bb39a-5497-412b-9b44-d190de36b173&s=pc&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWwy"
        self.headers_part = {
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        self.text = self.get_response()
        if self.text is None:
            pass # Program ends
        else:
            self.scrape_data(self.text)

    def get_response(self):
        while True:
            response = requests.get(url=self.BASE_URL, headers=self.headers_part)
            if response.status_code == 200:
                print("Response status succesfull")
                return response.text
            else:
                print("Choose what to do: ")
                choice = input("E - exit\nT - try again in 30 seconds\n")[0].lower()

                if choice == "e":
                    return None
                elif choice == "t":
                    time.sleep(30)
                else:
                    print("Wrong input - programm is shutting down..")
                    return None
    
    def scrape_data(self, text):
        soup = BeautifulSoup(text, "lxml")
        price = soup.select(".a-offscreen")[0].getText()
        title = soup.select("h1#title > span#productTitle")[0].getText().split(",")[0].strip()
        float_price = float(price[1:])

        if float(float_price) < 350:
            self.send_email(title, price)

    def send_email(self, title, price):
        email = AmazonPriceChecker.MY_EMAIL
        password = AmazonPriceChecker.PASSWORD
        email_text = f"{title}.\nNow: {price}.\nLink: {self.BASE_URL}"

        connection = smtplib.SMTP("smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(user=email, password=password) # type: ignore
        connection.sendmail(from_addr=email, to_addrs=email, msg=f"Subject:Amazon Price Alert!\n\n{email_text}")

AmazonPriceChecker()