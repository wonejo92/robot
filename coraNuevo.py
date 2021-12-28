from threading import current_thread
from telegram import update


def informacion_mensaje(mensaje):
    if "text" in mensaje["message"]:
        tipo = "texto"
    elif "sticker" in mensaje["message"]:
        tipo = "sticker"
    elif "animation" in mensaje["message"]:
        tipo = "animacion"
    elif "photo" in mensaje["message"]:
        tipo = "foto"
    else:

        tipo = "otro"

    persona = mensaje["message"]["from"]["first_name"]
    id_chat = mensaje["message"]["chat"]["id"]
    id_update = mensaje["update_id"]

    # Devolver toda la informacion
    return tipo, id_chat, persona, id_update


def leer_mensaje(mensaje):
    texto = mensaje["message"]["text"]
    return texto


def iniciarProcesos(algoo):
    while(True):
        mensajes_diccionario = update(algoo)
        print(mensajes_diccionario)
        for i in mensajes_diccionario["result"]:
            tipo, idchat, nombre, id_update = informacion_mensaje(i)
            print(idchat)
            if tipo == "texto":
                texto = leer_mensaje(i)
                print('texto recuperadoooo', texto)
                return 'adentro'

            if id_update > (ultima_id-1):
                ultima_id = id_update + 1

        mensajes_diccionario = []
