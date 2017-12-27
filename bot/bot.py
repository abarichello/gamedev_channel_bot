import logging, time
from telegram.ext import Updater, CommandHandler

import core
import config

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    def error_callback(bot, update, error):
        logging.error(error)
        bot.send_message(chat_id=config.DEBUG_CHANNEL, text=error)

    updater = Updater(token=config.DEV_TOKEN)
    dp = updater.dispatcher
    job = updater.job_queue

    dp.add_error_handler(error_callback)
    dp.add_handler(CommandHandler('start', core.start))
    dp.add_handler(CommandHandler('parse', core.parse))
    dp.add_handler(CommandHandler('help', core.get_help))

    core.parse(updater.bot)
    print(time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.gmtime()))
    time.sleep(1200) # Sleep for 1 hour

    # updater.start_webhook(listen='0.0.0.0', port=config.PORT, url_path=config.DEV_TOKEN)
    # updater.bot.setWebhook("https://" + config.APPNAME + ".herokuapp.com/" + config.DEV_TOKEN)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
