import requests
from bs4 import BeautifulSoup
import threading
from Car import Car
from TelegramBot import TelegramBot
from OneTimePassword import OneTimePassword

FETCH_NEW_DATA_PERIOD = 60 * 5  # Every 5 minuets
sent_cars_tokens = []
telegram_bot: TelegramBot
TELEGRAM_BOT_TOKEN = "870895817:AAGo3vzpDx9yCrZ-JS-xiNpywL78gj-SLIc"
owner_telegram_id = 105219253
bot_users_ids = []
one_time_password: OneTimePassword


def get_cities():
    response = requests.get("https://divar.ir/")
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            city_elements = soup.select(
                ".city-group:nth-of-type(3) .ui.button")
            return [(str(city_element["href"]).split('/')[-1])
                    for city_element in city_elements]
        except:
            print("Something went wrong in the process of fetching cities.")


def fetch_and_send_cars(city):
    search_result = requests.get(
        f"https://api.divar.ir/v8/web-search/{city}/car?q=تصادفی")
    if search_result.status_code != 200:
        return

    for c in search_result.json()["widget_list"]:
        if c["data"]["token"] not in sent_cars_tokens and (
                c["data"]["normal_text"].startswith("دقایقی پیش") or "فوری" in c["data"]["red_text"]):

            car = Car(c["data"]["token"], c["data"]["title"],
                      c["data"]["description"], c["data"]["city"],
                      c["data"]["district"], c["data"]["image"])

            text = f"[{car.title}]({car.link()})\n\n[{car.city}" \
                   f"-{car.district if car.district is not None else ''}]({car.image_url})\n\n_{car.price}_"
            for user_id in bot_users_ids:
                telegram_bot.send_text(user_id, text)
            sent_cars_tokens.append(c["data"]["token"])
        elif c["data"]["token"] in sent_cars_tokens and not c["data"]["normal_text"].startswith(
                "دقایقی پیش") and "فوری" not in c["data"]["red_text"]:
            sent_cars_tokens.remove(c["data"]["token"])


def on_telegram_message_received(update, context):
    sender_id = update.effective_chat["id"]
    sender_text = update.message.text

    if sender_id == owner_telegram_id and "code" in sender_text:
        auth_code = one_time_password.get_new_code()
        telegram_bot.send_text(owner_telegram_id, text=auth_code)

    else:
        if one_time_password.verify_code(sender_text):
            if sender_id in bot_users_ids:
                bot_users_ids.remove(sender_id)
                telegram_bot.send_text(
                    sender_id, text="`شما از لیست دریافت گنندگان حذف شدید.`")
            else:
                bot_users_ids.append(sender_id)
                telegram_bot.send_text(
                    sender_id, text="`شما به لیست دریافت گنندگان اضافه شدید.`")
        else:
            telegram_bot.send_text(sender_id, text="`کد اشتباه است.`")


def main(cities):
    threading.Timer(FETCH_NEW_DATA_PERIOD, main, args=(cities,)).start()
    if bot_users_ids:
        for city in cities:
            threading.Thread(target=fetch_and_send_cars, args=(city,)).start()
    else:
        print("No subscriber.")


if __name__ == "__main__":
    telegram_bot = TelegramBot(
        TELEGRAM_BOT_TOKEN, on_telegram_message_received)
    one_time_password = OneTimePassword()
    main(get_cities())
