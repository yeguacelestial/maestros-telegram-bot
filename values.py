import os
from telegram.ext import Updater
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher