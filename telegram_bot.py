import os

import telegram


def bot_message(article_link, article_title):
    bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_API"))
    bot.send_message(chat_id='@nasa_photo_lesson', text=f"*{article_title}*\n\nИсточник - Shazoo:\n{article_link}",
                     parse_mode=telegram.ParseMode.MARKDOWN)
