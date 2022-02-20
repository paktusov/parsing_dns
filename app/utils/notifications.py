import datetime as dt
import telebot
from twilio.rest import Client
from config import telegram_config, twilio_config


def send_sms(sms_text):
    client = Client(twilio_config.account_sid, twilio_config.auth_token)
    message = client.messages.create(
        to=twilio_config.to,
        from_=twilio_config.from_,
        body=sms_text
    )
    return message.sid


def send_photo_to_telegram(product, city):
    bot = telebot.TeleBot(getattr(telegram_config, 'token_' + city))
    last_price = product['history_price'][-1][0]
    #last_update_fmt = dt.datetime.fromisoformat(product['last_update']).strftime("%Y.%m.%d %H:%M")
    caption = '<a href="{}">{}</a>\n\n{}\n\n{} р. | {} р.\n\n{}'
    format_caption = caption.format(product['link'],
                                    product['name'],
                                    product['description'],
                                    last_price,
                                    product['full_price'],
                                    product['last_update']
                                    )
    bot.send_photo(telegram_config.id, photo=product['image'], caption=format_caption, parse_mode='HTML')
