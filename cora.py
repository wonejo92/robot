from threading import current_thread

from telegram import update
import telegram
import DB_utility
import procesos
import correo



conexion = DB_utility.DBConnector()
optionMenu = {}

bandera = bool

def initialMessage(input_text):
    global currentUser
    global bandera
    bandera = True
    user_message =  str(input_text).lower()
    print('recuperando',user_message)
    if user_message == '1':
        return 'Hola necesito tu Cedula de identidad.'
    if bandera == True:
        obtenerDatos(user_message)
        bandera = False
    if currentUser is not None:
        if user_message == currentUser['cedula']:
            correo.send_email(currentUser['correo'], currentUser['token'])
            return 'Ingresa el codigo de verificacion que se envio a tu correo electronico !!'
    
    if user_message == currentUser['token']:
        return '¿ Como te ayudo ? \n\n 1. Agendar una cita \n 2. Consulta de cuenta \n 3. Consulta de millas \n 4. Bloqueo de Tarjetas \n 5 Desbloqueo de tarjetas \n 6 Consultas Generales \n 7 Dejar un comentario \n'
    return 'No se ha registrado'


def obtenerDatos(input_text):
    global currentUser
    cedula = input_text
    user = conexion.execute_query(
        conexion.sql_dict.get('getClient'), (cedula,))
    id = user[0][0]
    cedula = user[0][1]
    nombres = user[0][2]
    apellidos = user[0][3]
    email = user[0][4]
    token = user[0][5]
    currentUser = {"id": id, "cedula": cedula, "nombres": nombres,
                   "apellidos": apellidos, "correo": email, "token": token}
    return currentUser

def info_mensaje(mensaje):
 
    #Comprobar el tipo de mensaje
    
    print (mensaje)
    try:
        if "text" in mensaje["message"]:
            tipo = "texto"
        elif "sticker" in mensaje["message"]:
            tipo = "sticker"
        elif "animation" in mensaje["message"]:
            tipo = "animacion" #Nota: los GIF cuentan como animaciones
        elif "photo" in mensaje["message"]:
            tipo = "foto"
        else:
            tipo = "otro"

        persona = mensaje["message"]["from"]["first_name"]
        id_chat = mensaje["message"]["chat"]["id"]
        id_update = mensaje["update_id"]
    except Exception as e:
            tipo = "otro"
            persona = ""
            id_chat = 0
            id_update = 0
    return tipo, id_chat, persona, id_update


def leer_mensaje(mensaje):
    texto = mensaje['message']['text']
    return texto


ultima_id = 0
def recuperarMensaje():
    mensajes_diccionario = update(ultima_id)
    print('diccionario',mensajes_diccionario)
    for i in mensajes_diccionario['result']:
        tipo, idchat, nombre, id_update = info_mensaje(i)
        if tipo == 'texto':
            texto = leer_mensaje(i)
            return texto

def showMenu():
    print('¿ Como te ayudo ? \n\n'
          '1. Agendar una cita \n'
          '2. Consulta de cuenta \n'
          '3. Consulta de millas \n'
          '4. Bloqueo de Tarjetas \n'
          '5 Desbloqueo de tarjetas \n'
          '6 Consultas Generales \n'
          '7 Dejar un comentario \n')

    optionMenu = {"1": "Agendar_Cita", "2": "Consulta_Cuenta", "3": "Consulta_Millas", "4": "Bloqueo_Tarjeta", "5":
                  "Desbloqueo_Tarjeta", "6": "Consultas_Generales", "7": "Dejar_Comentario"}

    answerMenu = input()
    print(optionMenu[answerMenu])
    match optionMenu[answerMenu]:
        case "Agendar_Cita":
            procesos.Agendar_Cita()
            showMenu()
        case "Consulta_Cuenta":
            procesos.Consulta_Cuenta()
            showMenu()
        case "Consulta_Millas":
            procesos.obtenerMillas()
            showMenu()
        case "Bloqueo_T4arjeta":
            procesos.bloqueoDesbloqueoTarjeta('bloquear')
            showMenu()
        case "Desbloqueo_Tarjeta":
            procesos.bloqueoDesbloqueoTarjeta('desbloquear')
            showMenu()
        case "Consultas_Generales":
            procesos.Consultas_Generales()

initialMessage('1')