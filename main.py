from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

import logging
import logging.config

from tests import Jet5Test
from tests import StatusTypes
from test_data import TestData

# Logger
logging.config.fileConfig('logging.conf')
logger = logging.getLogger("jet5TelegramBot")

# Stages
START_VALIDATOR, SECOND = range(2)
# Callback data
# START_VALIDATOR, TWO, THREE, FOUR = range(4)


def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Start validator", callback_data='0'),
            InlineKeyboardButton("Option 2", callback_data='1'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='2')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def validate_form(update: Update, context: CallbackContext) -> None:
    test_data = TestData()
    print(test_data.set_negative())

    update.message.reply_text("Validation started 🕑")

    jet5 = Jet5Test(test_data)
    feedback_status = jet5.validate()

    if feedback_status == StatusTypes.complete:
        logger.info("All data sent successfully")
        update.message.reply_text("All data sent successfully ✔")
    elif feedback_status == StatusTypes.error_data:
        logger.error("Wrong data")
    elif feedback_status == StatusTypes.error_loading_time:
        logger.error("Timeout error")
        update.message.reply_text("❌ Timeout error ❌")
        update.message.reply_photo(photo=open('./screenshots/pageImage.png', 'rb'), caption="pageImage.png")
        update.message.reply_photo(photo=open('./screenshots/element.png', 'rb'), caption="element.png")



def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2107198393:AAESWAU68Z046f0TxdgWEczxer1tHLTg7ow")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("validate_form", validate_form))

    # Start the Bot
    updater.start_polling()
    logger.debug("Bot Started")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
    # test_data = TestData()
    # print(test_data.set_positive())
    #
    # jet5 = Jet5Test(test_data)
    # jet5.validate()
