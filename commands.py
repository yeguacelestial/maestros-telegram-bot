from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from bs4 import BeautifulSoup

from values import updater, dispatcher
from screenshot import capture
from fuzzywuzzy import fuzz

import random
import requests
import time

def activate_commands():
    # Add commands
    add_command(start)
    add_command(maestro)
    add_command(materia)
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
                            "Escribe /ayuda para ver los comandos disponibles."
    )

def maestro(update, context):
    nombre = "-".join(context.args)

    try:
        cantidad = int(context.args[-1])

        if cantidad <= 0:
            context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text=f"Ehm, no tiene mucho sentido tu valor de {cantidad}... ¿Necesitas /ayuda?")
            return
        
        else:
            pass

    except ValueError as e:
        cantidad = 1

    except IndexError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f"¡Dime el nombre de algun maestro! En /ayuda te doy más información sobre cómo funciono.")
        return


    URL_FIME = f'http://www.listademaestros.com/fime/buscar/{nombre}'

    # Parse info from HTML
    response = requests.get(URL_FIME)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    # Maestros listing
    maestros_list = soup.find_all('td', {'class':'results_left_td'})

    # Final postings
    final_postings = []

    for maestro in maestros_list[1:]:
        maestro_name = maestro.a.text
        maestro_link = maestro.a.get('href')
        chidos = maestro.find(class_="result_chido_score").text
        gachos = maestro.find(class_="result_gacho_score").text

        final_postings.append((maestro_name, maestro_link, chidos, gachos))

    # Output message
    if len(final_postings) > 0 and cantidad > 0:
        for maestro in final_postings[:cantidad]:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                    text=f"<a href='{maestro[1]}'><b>{maestro[0]}</b></a>\n\n"+
                                        f"👍 <b><i>Chidos:</i></b> {maestro[2]}\n\n"+
                                        f"👎 <b><i>Gachos:</i></b> {maestro[3]}",
                                    parse_mode='HTML')
    
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="¡No se encontraron resultados! ☹️")

def materia(update, context):
    # Filtering and replacing data
    materia = " ".join(context.args)
    materia = materia.replace('1', 'I')
    materia = materia.replace('2', 'II')
    materia = materia.replace('3', 'III')
    materia = materia.replace('4', 'IV')
    materia = materia.replace('5', 'V')
    materia = materia.lower()

    # URLs
    url_horarios = 'https://horarios.fime.me'
    url_dependencia_fime = f'{url_horarios}/dependencia/2316'
    url_periodo = None

    # Parse info from HTML
    response = requests.get(url_dependencia_fime)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    # Get last term
    last_term = soup.find_all('li', {'class': 'feature sombra-blanca'})[0]
    last_term_link = last_term.a['href']

    url_last_term = url_horarios + last_term_link

    # First letter of materia
    first_letter_materia = "/materias/" + materia[0]
    current_url = url_last_term + first_letter_materia + "/"

    # Fetch all materias
    response = requests.get(current_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    materias = soup.findAll('li', { 'class': 'feature sombra-blanca' })

    materias_dict = {}
    for m in materias:
        materias_dict.update({m.text: m.a['href']})
    
    materias_nombres = []
    materias_links = []
    for k,v in materias_dict.items():
        materias_nombres.append(k)
        materias_links.append(v)

    matches = []
    for nombre in materias_nombres:
        nombre = nombre.lower()
        nombre = nombre.replace('á', 'a')
        nombre = nombre.replace('é', 'e')
        nombre = nombre.replace('í', 'i')
        nombre = nombre.replace('ó', 'o')
        nombre = nombre.replace('ú', 'u')

        matches.append(fuzz.ratio(nombre, materia))
    
    try:
        maxIndex = matches.index(max(matches))
        materia_elegida = materias_nombres[maxIndex]
        url_final = url_horarios + materias_links[maxIndex]
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=f"No se encontraron resultados de '{materia}'.")
        return

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Buscando {materia}...")
    capture(url_final)
    context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=f"Mostrando la materia: <a href='{url_final}'><b>{materia_elegida}</b></a>",
                            parse_mode="HTML")
    context.bot.send_photo(chat_id=update.effective_chat.id, text=" ".join(context.args), photo=open('listado.png', 'rb'))

def ayuda(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                text="<b>Comandos disponibles y uso</b>\n\n"+
                "/maestro [nombre del maestro] [resultados]\n <i>Chidos y gachos del maestro especificado.</i>\n\n"+
                "/materia [nombre de la materia]\n <i>Horarios disponibles de la materia</i>\n\n"+
                "/ayuda\n<i>Comandos disponibles del bot</i>",
                parse_mode='HTML')