import os
try:
    from telethon.sync import TelegramClient
    from telethon import TelegramClient, events, sync
    from telethon import functions, types
    from telethon.tl.types import PeerUser, PeerChat, PeerChannel
except:
    os.system('pip install telethon')
    from telethon.sync import TelegramClient
    from telethon import TelegramClient, events, sync
    from telethon import functions, types


import requests as req
import json
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:/Users/manue/AppData/Local/tesseract/tesseract.exe'
from PIL import Image
import os



# DATOS ACCESO TELEGRAM
bot = 'TelethonHelp'
api_id= 3799542
api_hash='f2acae7f6de51d732e65c688217ae943'
client= TelegramClient(bot,api_id,api_hash)


client.start()
parametro = None
# entity = client.get_entity('blakithomson') #Especificar de qué usuario quieres obtener los mensajes
entity = client.get_entity('ampisb') #Especificar de qué usuario quieres obtener los mensaje

@client.on(events.NewMessage)
async def my_event_handler(event):
    # parametro =  awaitparametro.append(event.raw_text)
    # print(parametro)
    # print(event)
    # await event.download_media(file="recibido")
    # with open("event.txt", "w") as fichero:
    #     fichero.write(str(event))
    if event.message.peer_id.user_id == entity.id:
        if event.media:
            await event.download_media("recibido.jpg")
            print("Imagen Recibida")
        elif event.raw_text:
            parametro = event.raw_text
            print(parametro)


    token = "84381-WNORmsIhPggysY"

    pagina = range(1,11)
    #! CREACION DE TODOS LOS EVENTOS UPCOMING...
    termina = False
    lista = []
    for numero in pagina:
        if termina == False:
            response = req.get(f"https://api.b365api.com/v1/bet365/upcoming?sport_id=1&page={numero}&per_page=100&token={token}").json()["results"]
            if response != []:
                for event in response:
                    lista.append(event)
            if response == []:
                termina = True
    with open("upcoming.json", "w", encoding='utf8') as fichero:
        json.dump(lista, fichero, ensure_ascii=False)
    #! FIN CREACION DE UPCOMING.JSON

    imagen = Image.open("recibido.jpg")
    texto = tess.image_to_string(imagen)
    numeros = ["0","1","2","3","4","5","6","7","8","9"]

    #! SEPARAMOS LOS ELEMENTOS DE LA IMAGEN POR SALTO DE LINEA, EN UNA LISTA
    lista = texto.split("\n")[0:-1]

    #! INICIO: MANEJO DEL NOMBRE DEL EQUIPO
    nombre_equipo = lista[0]
    if "+" in nombre_equipo:
        nombre_equipo = nombre_equipo.split("+")[0]
    elif "-" in nombre_equipo:
        nombre_equipo = nombre_equipo.split("-")[0]
    else:
        for numero in numeros:
            if numero in nombre_equipo:
                nombre_equipo = nombre_equipo.replace(numero, "")
        if "." in nombre_equipo:
            nombre_equipo = nombre_equipo.replace(".", "")

    if nombre_equipo.endswith(" "):
        nombre_equipo = nombre_equipo[:-1]
        if nombre_equipo.endswith(" "):
            nombre_equipo = nombre_equipo[:-1]
    #! FIN DE MANEJO DEL NOMBRE

    nombre_apuesta = texto.split("\n")[1]
    #! ^^ POSICIÓN 1 (SEGUNDA POSICION DE LA LISTA) - TIPO DE APUESTA ^^
    print([nombre_equipo])
    print([nombre_apuesta])

    found = False
    with open("upcoming.json", "r") as upcoming:
        contenido_upcoming = json.load(upcoming)
        for evento in contenido_upcoming:
            if found == False:
                if evento["home"]["name"] == nombre_equipo or evento["away"]["name"] == nombre_equipo:
                    found = True
                    event_id = evento["id"]
        if found == False:
            print("Equipo no se encuentra en upcoming.json")
    # print(event_id)
    asian_line = ["Asian Handicap", "Alternative Asian Handicap"]
    main = ["Full Time Result", "Double Chance"]

    url_adic = ""
    if nombre_apuesta in asian_line:
        url_adic = "I3/"
    elif nombre_apuesta in main:
        url_adic = ""
    os.system(f"python -m webbrowser -t www.bet365.es/#/AC/B1/C1/D8/E{event_id}/F3/{url_adic}")


client.run_until_disconnected()