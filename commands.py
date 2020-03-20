from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from values import updater, dispatcher
import random

def activate_commands():
    # Add commands
    add_command(start)

    # Handling unknown commands
    def unknown(update, context):
        words = [
            '¿Qué quieres decir? 🤔 Pide /ayuda para ver los comandos disponibles.',
            'Lo desconozco...¿Buscas /ayuda?', 
            '¡No es uno de mis comandos! ¿Necesitas /ayuda?', 
            'Escribe /ayuda para ver los comandos disponibles.',
            'Un poco de /ayuda podría ser útil...',
            '😶'
            ]
        mensaje = random.choice(words)
        context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje)

    unknown_handler = MessageHandler(Filters.text, unknown)
    dispatcher.add_handler(unknown_handler)

def add_command(function):
    handler = CommandHandler(function.__name__, function)
    dispatcher.add_handler(handler)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=
                            "¡Bienvenido al bot de Lista de Maestros!\n"+
                            "Escribe \ para ver los comandos disponibles."
    )
