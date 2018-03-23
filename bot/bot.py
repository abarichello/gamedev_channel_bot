import logging, datetime
from telegram.ext import Updater, CommandHandler, JobQueue

import time
import core
import config

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.CRITICAL)
    logger = logging.getLogger(__name__)

    def error_callback(bot, update, error):
        logging.error(error)

    updater = Updater(token=config.DEV_TOKEN)
    job = updater.job_queue
    dp = updater.dispatcher

    dp.add_error_handler(error_callback)
    dp.add_handler(CommandHandler('start', core.start))
    dp.add_handler(CommandHandler('help', core.get_help))

    while True:
        if datetime.datetime.now().minute is 0:  # Wait for next hour
            job.run_repeating(core.parse, interval=3600, first=0)
            break
        else:
            time.sleep(10)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
