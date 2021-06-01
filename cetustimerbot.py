#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time




# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def report(update, context):
    url = "https://hub.warframestat.us/#/"
    driver = webdriver.Chrome('C:/Users/niiod/Downloads/chromedriver_win32/chromedriver.exe')
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


    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()