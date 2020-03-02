import requests
import telegram
from telegram.ext import Updater
from bs4 import BeautifulSoup
import threading
from Car import Car

cities = []
sent_cars_tokens = []
updater = Updater(
    token='870895817:AAGo3vzpDx9yCrZ-JS-xiNpywL78gj-SLIc', use_context=True)
user_telegram_id = 105219253


def get_cities():
    global cities
    response = requests.get("https://divar.ir/")
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            city_elements = soup.select(".city-group:nth-of-type(3) .ui.button")
            cities = [(str(city_element["href"]).split('/')[-1])
                      for city_element in city_elements]
        except:
            pass


def fetch_and_send_cars(city):
    search_result = requests.get(
        f"https://api.divar.ir/v8/web-search/{city}/car?q=تصادفی")
    if search_result.status_code != 200:
        return

    cars = []
    for c in search_result.json()["widget_list"]:
        if c["data"]["token"] not in sent_cars_tokens and (
                c["data"]["normal_text"].startswith("دقایقی پیش") or "فوری" in c["data"]["red_text"]):
            cars.append(Car(c["data"]["token"], c["data"]["title"],
                            c["data"]["description"], c["data"]["city"],
                            c["data"]["district"], c["data"]["image"]))
            sent_cars_tokens.append(c["data"]["token"])
        elif c["data"]["token"] in sent_cars_tokens and not c["data"]["normal_text"].startswith(
                "دقایقی پیش") and "فوری" not in c["data"]["red_text"]:
            sent_cars_tokens.remove(c["data"]["token"])

    send_messages(cars)


def send_messages(cars):
    try:
        for car in cars:
            text = f"[{car.title}]({car.link()})\n\n[{car.city}-{car.district if car.district is not None else ''}]({car.image_url})\n\n_{car.price}_"
            updater.bot.send_message(chat_id=user_telegram_id,
                                     text=text,
                                     parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        pass


def main():
    threading.Timer(60 * 3, main).start()
    for city in cities:
        threading.Thread(target=fetch_and_send_cars, args=(city,)).start()


if __name__ == "__main__":
    get_cities()
    updater.start_polling()
    main()
    updater.stop()
