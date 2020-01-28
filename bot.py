from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram, logging
import os

token = os.environ['TELEGRAM_TOKEN']
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    # starts bot and shows instructions
    update.message.reply_text("Hi, I'm a bot to welcome new group members! To set your custom welcome message, type:\n\n /setup [message]")


def setup(update, context):
    # separates command and message
    welcome_message = update.message.text.partition(' ')[2]
    # stores message
    context.chat_data[0] = welcome_message
    update.message.reply_text("Welcome message set to:\n\n" + context.chat_data[0])


def display(update, context):
    try:
        # displays message if already set
        welcome_message = context.chat_data[0]
        update.message.reply_text(welcome_message)

    except KeyError:
        update.message.reply_text("Welcome message not defined yet")


def welcome(update, context):
    try:
        # gets the username to tag new member in the welcome message
        user_id = "@" + update.message.new_chat_members[0].username
    except Exception:
        # user has no @
        user_id = update.message.new_chat_members[0].first_name

    try:
        # when someone enters the group, message is sent by bot
        update.message.reply_text(user_id + "\n\n" + context.chat_data[0])
    except Exception:
        # if message not set
        return

    
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def unknown(update, context):
    # if user sends not defined command
    bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def main():
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('setup', setup))
    dp.add_handler(CommandHandler('display', display))

    # listens for new group members
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    dp.add_error_handler(error)
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()

    updater.idle()

if __name__ == "__main__":
    main()
