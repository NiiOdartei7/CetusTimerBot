#!/usr/bin/env python
# -*- coding: utf-8 -*-



import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import os




# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
PORT = int(os.environ.get('PORT', '8443'))

 
def report(update, context):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    url = "https://hub.warframestat.us/#/"
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(url)
    time.sleep(5)

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    all_divs = soup.find('div', {'class': 'panel-header packery-item mt-2 time col-md-4 cetus'})
    span_find = all_divs.find_all('span')
    cetus_status = span_find[1]
    cetus_time = span_find[2]
    botTimer = cetus_time.get_text()
    botStatus = cetus_status.get_text()

    update.message.reply_text(botTimer)
    update.message.reply_text(botStatus)


    driver.close()  # closing the webdriver

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1892423720:AAHjtdCH_-zz6UPYTnEH8s_vSm22mG0l58A", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", report))

    # Run bot

 # webhook mode
    print(f"Running bot in webhook mode. Make sure that this url is correct: https://cetusbot.herokuapp.com/")
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="1892423720:AAHjtdCH_-zz6UPYTnEH8s_vSm22mG0l58A",
        webhook_url=f"https://cetusbot.herokuapp.com/1892423720:AAHjtdCH_-zz6UPYTnEH8s_vSm22mG0l58A"
    )

#    updater.bot.set_webhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/{TELEGRAM_TOKEN}")
    updater.idle()
  
    


if __name__ == '__main__':
    main()
