import os
import logging
from dotenv import load_dotenv
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

def main():
    # Main bot config
    load_dotenv()
    TOKEN = os.getenv('TOKEN')

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s -%(message)s',
                        level=logging.INFO)

    # Create commands
    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Prueba")
    
    def echo(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    
    def caps(update, context):
        text_caps = ' '.join(context.args).upper()
        print(text_caps)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

    # COMMANDS
    # Start command
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Returns message in CAPS
    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)

    # Echo all text messages (echo handling)
    echo_handler = MessageHandler(Filters.text, echo) # Filters class filter messages for text, images, status, etc
    dispatcher.add_handler(echo_handler)
    
    # Start to poll
    updater.start_polling()

if __name__ == '__main__':
    main()