from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from values import updater, dispatcher
import random
import time

def activate_commands():
    # Add commands
    add_command(start)
    add_command(maestro)
    add_command(ayuda)

    # Handling unknown commands
    def unknown(update, context):
        words = [
            '¿Qué quieres decir? 🤔 Pide /ayuda para ver los comandos disponibles.',
            'Lo desconozco...¿Buscas /ayuda?', 
            '¡No es uno de mis comandos! ¿Necesitas /ayuda?', 
            'Escribe /ayuda para ver los comandos disponibles.',
            'Un poco de /ayuda podría ser útil...',
            '😶 /ayuda'
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

def maestro(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                            text=
                            "<a href='listademaestros.com'><b>NOMBRE DEL MAESTRO</b></a>\n\n"+
                            "👍 <b><i>Chidos:</i></b> 1212412\n\n"+
                            "👎 <b><i>Gachos:</i></b> 999999",
                            parse_mode='HTML')
    time.sleep(5)
    context.bot.send_message(chat_id=update.effective_chat.id, text=" ".join(context.args))

def ayuda(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="<b>Comandos disponibles</b>\n\n"+
                                   "/maestro [nombre del maestro]\n <i>Información sobre el maestro</i>\n\n"+
                                   "/materia [nombre de la materia]\n <i>Horarios disponibles de la materia</i>\n\n"+
                                   "/ayuda\n<i>Comandos disponibles del bot</i>",
                             parse_mode='HTML')