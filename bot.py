from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler, MessageHandler, filters

import logging
import settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='bot.log',
    level=logging.INFO
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='bot.log',
    level=logging.INFO
)

# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("User %s started the conversation.", update.message.from_user)

    keyboard = [
        [InlineKeyboardButton("Exchange rates", callback_data="1")],
        [InlineKeyboardButton("Cryptocurrency rates", callback_data="2")],
        [InlineKeyboardButton("Stock prices", callback_data="3")],
        [InlineKeyboardButton("Help", callback_data="4")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"Hello, {update.effective_user.name}. I'm a bot! Please choose:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info(update)

    query = update.callback_query

    await query.answer()

    await query.delete_message()

    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = f"Selected option: {query.data}"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info(update)

    text = f"Hello, {update.effective_user.name}. I'm a bot, please talk to me!"

    await update.message.reply_text(text)

#async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    logging.info(update)
#    await context.bot.send_message(
#        chat_id = update.effective_chat.id,
#        text = f"Hello, {update.effective_user.name}. I'm a bot, please talk to me!"
#    )

#async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    logging.info(update)
#    await context.bot.send_message(
#        chat_id = update.effective_chat.id,
#        reply_to_message_id = update.effective_message.message_id,
#        text = f"I'm help you, {update.effective_user.name}"
#    )

#async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    logging.info(update)
#    await context.bot.send_message(
#        chat_id = update.effective_chat.id,
#        reply_to_message_id = update.effective_message.message_id,
#        text = update.message.text
#    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(settings.bot_token).build()
    
    #echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CallbackQueryHandler(button))
    
    application.run_polling()