from uuid import uuid4

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup, \
    InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext, InlineQueryHandler, CallbackQueryHandler,
)

import logging
import logging.config

from telegram.utils.helpers import escape_markdown

from tests import Jet5Test
from tests import StatusTypes
from test_data import TestData

# Logger
logging.config.fileConfig('logging.conf')
logger = logging.getLogger("jet5TelegramBot")

# Stages
MAIN_MENU, VALIDATOR_MENU, LOGGER = range(3)


def main_menu_keyboard():
    return [
        [InlineKeyboardButton("Validator", callback_data='validator_menu')],
        [InlineKeyboardButton("Logger", callback_data='logger_menu')]
    ]


def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = main_menu_keyboard()

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

    return MAIN_MENU


def start_over(update, _) -> None:
    """Тот же текст и клавиатура, что и при `/start`, но не как новое сообщение"""
    # Получаем `CallbackQuery` из обновления `update`
    query = update.callback_query
    # На запросы обратного вызова необходимо ответить,
    # даже если уведомление для пользователя не требуется.
    # В противном случае у некоторых клиентов могут возникнуть проблемы.
    query.answer()

    """Sends a message with three inline buttons attached."""
    keyboard = main_menu_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Please choose:', reply_markup=reply_markup)

    return MAIN_MENU


def validate_form(update, context: CallbackContext) -> None:
    """Starts jet5 form validator"""
    # Generate test data
    test_data = TestData()
    test_data.set_negative(random_field=True)

    update.edit_message_text("Validation started 🕑")

    jet5 = Jet5Test(test_data)
    feedback_status = jet5.validate()

    if feedback_status == StatusTypes.complete:
        update.message.reply_text("All data sent successfully ✔")
    elif feedback_status == StatusTypes.error_data:
        update.message.reply_text("❌ Wrong data ❌")
        update.message.reply_photo(photo=open('./screenshots/pageImage.png', 'rb'), caption="pageImage.png")
        update.message.reply_photo(photo=open('./screenshots/element.png', 'rb'), caption="element.png")
    elif feedback_status == StatusTypes.error_loading_time:
        update.message.reply_text("❌ Timeout error ❌")
        update.message.reply_photo(photo=open('./screenshots/pageImage.png', 'rb'), caption="pageImage.png")
        update.message.reply_photo(photo=open('./screenshots/element.png', 'rb'), caption="element.png")


def validator_menu(update, _):
    """Показ нового выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Validate Positive", callback_data=str("positive"))],
        [InlineKeyboardButton("Validate Negative", callback_data=str("negative"))],
        [InlineKeyboardButton("Back", callback_data=str("back"))],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Validator Menu: ", reply_markup=reply_markup
    )
    return VALIDATOR_MENU


def validator_negative(update: Update, context: CallbackContext):
    """Показ нового выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Validate Positive", callback_data=str("positive"))],
        [InlineKeyboardButton("Validate Negative", callback_data=str("negative"))],
        [InlineKeyboardButton("Back", callback_data=str("back"))],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    validate_form(query, context)

    query.message.reply_text(
        text="Validator Menu: ", reply_markup=reply_markup
    )
    # query.message.reply_text('Please choose:')
    return VALIDATOR_MENU


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2107198393:AAESWAU68Z046f0TxdgWEczxer1tHLTg7ow")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(validator_menu, pattern='^' + str("validator_menu") + '$'),
                # CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
            ],
            VALIDATOR_MENU: [
                CallbackQueryHandler(validator_negative, pattern='^' + str("negative") + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str("back") + '$'),
                # CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
            ],
            # LOGGER: [
            #     CallbackQueryHandler(validate_form, pattern='^' + str("validate") + '$'),
            #     # CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
            #     # CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
            # ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    logger.debug("Bot Started")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
