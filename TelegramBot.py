import telegram
from telegram.ext import Updater, MessageHandler, Filters


class TelegramBot:
    def __init__(self, bot_token, on_message_received_callback=None):
        self.updater = Updater(token=bot_token, use_context=True)

        if on_message_received_callback:
            self.dispatcher = self.updater.dispatcher
            message_received_handler = MessageHandler(Filters.text, on_message_received_callback)
            self.dispatcher.add_handler(message_received_handler)

        try:
            self.updater.start_polling()
        except:
            print("Something went wrong while starting the bot.")

    def __del__(self):
        try:
            self.updater.stop()
        except:
            print("Something went wrong while stopping the bot.")

    def send_text(self, chat_id, text):
        try:
            self.updater.bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            print(f"Unexpected error during sending message to {chat_id}.")
