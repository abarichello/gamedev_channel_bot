import logging
from telegram.ext import Updater, CommandHandler, JobQueue

import core
import config

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    def error_callback(bot, update, error):
        logging.error(error)

    updater = Updater(token=config.DEV_TOKEN)
    job = updater.job_queue
    dp = updater.dispatcher

    dp.add_error_handler(error_callback)
    dp.add_handler(CommandHandler('start', core.start))
    dp.add_handler(CommandHandler('help', core.get_help))

    job.run_repeating(core.parse, interval=3600, first=0)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
