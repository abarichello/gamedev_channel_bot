import logging, time
from telegram.ext import Updater, CommandHandler

import core
import config

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    def error_callback(bot, error):
        logging.error(error)
        bot.send_message(chat_id=config.DEBUG_CHANNEL, text=error)

    updater = Updater(token=config.DEV_TOKEN)
    dp = updater.dispatcher

    dp.add_error_handler(error_callback)
    dp.add_handler(CommandHandler('start', core.start))
    dp.add_handler(CommandHandler('help', core.get_help))

    while True:
        core.parse(updater.bot)
        print(time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.gmtime()))
        time.sleep(3600) # Sleep for 1 hour

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
