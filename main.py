import RNN.RNN as funcionRNN
import logging
from os import curdir
import random
from typing import Text
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, constants, update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, conversationhandler,
                          )
import correo
import DB_utility
import correccion

conexion = DB_utility.DBConnector()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
# Estados
estadologin = 0
estadologinP1 = 0.1
estadologinP2 = 0.2
estadomenu = 1
estadoMenuP1 = 1.1
agendarCitaP1 = 2
agendarCitaP2 = 2.1
agendarCitaP3 = 2.2
agendarCitaP4 = 2.3
agendarCitaP6 = 2.4

consultarP1 = 3.1

tarjetaP2 = 4
tarjetaP4 = 4.2
analisisSentimiento=7.1



# Variables
user = {}
currentUser = {}
diasDisponibles = []
horasDisponibles = []
dias = []
day = ''
hour = ''
horas2 = []
millas = ''
estadoTarjeta = ''
tipoTarjeta = ''
mensajeTarjeta = ''



def start(update: Update, context: CallbackContext):
    """Starts the conversation and asks the user about their gender."""
    update.message.reply_text('Hola soy CORA 😉, tu asistente virtual !! \n\n '
                              '¿ Tienes cuenta con nosotros ? \n  SI \n  NO \n')
    return estadologin

# def cancel(update: Update, context: CallbackContext) -> int:
#     """Cancels and ends the conversation."""
#     user = update.message.from_user
#     logger.info("User %s canceled the conversation.", user.first_name)
#     update.message.reply_text(
#         'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
#     )
#     return ConversationHandler.END


"""Funciones para el logeo del cliente"""


def loginP1(update: Update, context: CallbackContext):
    text = update.message.text
    if(text == 'si'):
        update.message.reply_text('Ingresa tu Numero de Cedula !')
        return estadologinP1
    else:
        update.message.reply_text(
            'Procederemos a agendarte una cita para crearte una cuenta.')


def loginP2(update: Update, context: CallbackContext):
    global user
    try:
        cedula = update.message.text
        print("Mensaje en loginp2", cedula)        
        user = conexion.execute_query(
        conexion.sql_dict.get('getClient'), (cedula,))
        email = user[0][4]
        token = user[0][5]
        correo.send_email(email, token)
        update.message.reply_text('Ingresa el codigo que se te envio al correo Electronico registrado !')
        return estadologinP2
    except:
        update.message.reply_text('Algo salio mal revisa tu numero de celuda e ingresa de nuevo')



def loginP3(update: Update, context: CallbackContext):
    global user
    global currentUser
    codigo = update.message.text
    id = user[0][0]
    cedula = user[0][1]
    nombres = user[0][2]
    apellidos = user[0][3]
    email = user[0][4]
    token = user[0][5]
    if(codigo == token):
        # print("Persona Verificada")
        currentUser = {"id": id, "cedula": cedula, "nombres": nombres, "apellidos": apellidos, "correo": email,
                       "token": token}
        # print(currentUser)
        return menu(update, context)
    else:
        update.message.reply_text('No hemos encontrado tu cuenta !')



def menu(update: Update, context: CallbackContext):
    mensaje = 'Hola ' +currentUser["nombres"]+ '\t' + currentUser["apellidos"] + ' ! \n \n' + '¿ Como te ayudo ? \n\n 1. Agendar una cita \n 2. Consulta de cuenta \n 3. Consulta de millas \n 4. Bloqueo de Tarjetas \n 5. Desbloqueo de tarjetas \n 6. Consultas Generales \n 7. Dejar un comentario \n'
    update.message.reply_text(mensaje)
    return estadoMenuP1


def analisiSentimientos(update: Update, context: CallbackContext ):
    update.message.reply_text("Dejanos saber que te parecio nuestro servicio con un comentario. ")
    return analisisSentimiento

def analisiSentimientosP2(update: Update, context: CallbackContext ):
    text=update.message.text
    funcionRNN.predecir(text)
    



def menuP1(update: Update, context: CallbackContext):
    #text = update.message.text
    text =  correccion.procesamientoMensaje(update.message.text)
    #print(palabra)
    try:
         optionMenu = {"cita": "Agendar_Cita", "cuenta": "Consulta_Cuenta", "millas": "Consulta_Millas", "bloqueo": "Bloqueo_Tarjeta", "desbloqueo":
                  "Desbloqueo_Tarjeta", "generales": "Consultas_Generales", "comentario": "Dejar_Comentario"}
         match optionMenu[text]:
            case "Agendar_Cita":
                return citaP1(update, context)
       

            case "Consulta_Cuenta":
                return consultaCuentaP1(update,context)

            case "Consulta_Millas":
                return consultaMillasP1(update,context)

            case "Bloqueo_Tarjeta":
                global estadoTarjeta 
                estadoTarjeta = 'bloqueo'
                return bloqueoDesbloqueoTarjetaP1(update, context)

            case "Desbloqueo_Tarjeta":
                estadoTarjeta ='desbloqueo'
                return bloqueoDesbloqueoTarjetaP1(update, context)

            case "Consultas_Generales":
                update.message.reply_text('consultas generales')

            case "Dejar_Comentario":
                return analisiSentimientos(update,context)
    except:
        update.message.reply_text("Opcion incorrecta ingresa solo opciones del menu !!")
        return menu(update,context)

#--------------Agendar Cita------------------
def citaP1(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Procederemos ah agendarte una cita \n \n Estos son los días disponibles: ')
    return citaP2(update, context)

#Se muestran los dias disponibles
def citaP2(update: Update, context: CallbackContext):
    global diasDisponibles
    global dias
    horario = conexion.execute_query(conexion.sql_dict.get("getSchedule"), ())
    for i in range(len(horario)):
        diasDisponibles.append(horario[i][0])
    for j in range(len(diasDisponibles)):
        dias.append(diasDisponibles[j].capitalize())
    update.message.reply_text('\n'.join(map(str, dias)))
    #dias = ''
    return citaP3(update,context)



def citaP3(update: Update, context: CallbackContext):
    update.message.reply_text('Ingresa el dia para la cita')
    return agendarCitaP4
   

#se escoge el dia y se muestra el horario de acuerdo al dia elegido
def citaP4(update: Update, conetext: CallbackContext):
    global horasDisponibles
    global horas2
    global day
    try:
        day = update.message.text
        horas = conexion.execute_query(
            conexion.sql_dict.get("getHourSchedule"), (day,))
        mensaje = 'Horarios disponibles para el día: ' + day.capitalize()
        update.message.reply_text(mensaje)
        for h in range(len(horas)):
            horasDisponibles.append(horas[h][0])
        for k in range(len(horasDisponibles)):
            verHorario = str(k+1) +'.' + '\t' + horasDisponibles[k]
            horas2.append(verHorario)
        update.message.reply_text('\n'.join(map(str,horas2)))
        return citaP5(update,conetext)
    except:
        update.message.reply_text("Disculpa ese día no estoy disponible !")

def citaP5(update: Update, context: CallbackContext):
    update.message.reply_text('Ingresa la hora que necesites')
    return agendarCitaP6

#se registra la cita usando la fecha y la hora, y se da al usuario un codigo para que se presente ante las oficinas con el mismo
def citaP6(update: Update, context: CallbackContext):
    try:
        numHora = int(update.message.text)
        hora = horasDisponibles[numHora-1]
        consultaId=conexion.execute_query(conexion.sql_dict.get("getIdSchedule"),(day,hora))
        idhora=consultaId[0][0]
    except:
        update.message.text("Disculpa a esa hora no estoy disponible !")

    mensaje = 'Todo listo ! \n la cita se agendara a nombre de :\t' + currentUser["nombres"] + '\t' + currentUser["apellidos"]
    update.message.reply_text(mensaje)
    conexion.execute_query(conexion.sql_dict.get("defineSchedule"),(idhora,))
    conexion.execute_query('commit', None)
    codigoCita=random.randint(1000, 9999)
    conexion.execute_query(conexion.sql_dict.get("createAppointment"),(0,codigoCita,day,hora,'SI',currentUser["id"],idhora))
    conexion.execute_query('commit', None)
    mensaje2 = 'Genial tu cita está agendada 😊 \n Recuerda llegar 10 antes  con el siguiente codigo : '+'\t' + str(codigoCita)
    update.message.reply_text(mensaje2)

    return menu(update,context)

#--------------Consulta de cuenta------------------
def consultaCuentaP1(update: Update, context: CallbackContext):
    account=conexion.execute_query(conexion.sql_dict.get("accountInquiry"),(currentUser["nombres"],))
    mensaje = 'Número de cuenta: ' + account[0][0] + ' \n Fecha de creación: ' + account[0][1] + '\n Monto en USD: ' + str(account[0][2]) + '\n Tipo: ' + account[0][3]
    update.message.reply_text(mensaje)
    return menu(update,context)

#--------------Consulta de millas------------------
def consultaMillasP1(update: Update, context: CallbackContext):
    global millas 
    numeroTarjeta = conexion.execute_query(conexion.sql_dict.get("obtenerIdTarjeta"),(currentUser['id'],))
    cantidadMillas = conexion.execute_query(conexion.sql_dict.get('obtenerMillas'),(numeroTarjeta[0][0],))
    millas = cantidadMillas[0][0]
    mensaje = 'Sus millas son:'+ '\t' + str(cantidadMillas[0][0])
    update.message.reply_text(mensaje)
    return consultaMillasP2(update, context)

def consultaMillasP2(update: Update, context: CallbackContext):
    mensaje = premiosCanjeables(millas)
    update.message.reply_text(mensaje)
    return menu(update,context)
    


def premiosCanjeables(cantidadDeMillas):
    cantidadDeMillas = int(cantidadDeMillas)
    if cantidadDeMillas < 89 :
        return 'No cuentas actualmente con premios canjeables'
    if cantidadDeMillas <= 100 and cantidadDeMillas >= 90:
        return 'Felicidades ! acabas de ganar una orden de consumo de: \n 20.00 dolares en Pizza Hut, presentate en el establecimiento para \n reclamar el premio'
    if cantidadDeMillas <= 500 and cantidadDeMillas >= 300:
        return'Felicidades ! acabas de ganar un noche gratis en el hostal \n Rancho Dorado, acercate al hostal para reclamar tu premio'
    if cantidadDeMillas <= 5000 and cantidadDeMillas >= 4000:
        return 'Felicidades ! acabas de ganar un vuelo a Costa Rica de ida y vuelta ponte en contacto con nosotros para darte mas información'
    
#--------------Bloque/Desbloqueo de tarjeta según tipo------------------


def ejecutarSentencia(sentencia,parametro):
    dato = conexion.execute_query(conexion.sql_dict.get(sentencia),(parametro,))
    return dato

def ejecutarSentencia2(sentencia,parametro,parametro2):
    conexion.execute_query(conexion.sql_dict.get(sentencia), (parametro, parametro2,))
    conexion.execute_query('commit', None)
    

def bloquearDesbloquear(estado, tipo):
    if estado == 'bloqueo':
        if tipo == 'debito':
            ejecutarSentencia2('bloquearTarjeta', 'Debito', currentUser['id'])
            mensaje = 'Su tarjeta de débito ha sido bloqueada'
        if tipo == 'credito':
            ejecutarSentencia2('bloquearTarjeta', 'Credito', currentUser['id'])
            mensaje = 'Su tarjeta de crédito ha sido bloqueada'
    if estado  == 'desbloqueo':
        if tipo == 'debito':
            ejecutarSentencia2('desbloquearTarjeta', 'Debito', currentUser['id'])
            mensaje = 'Su tarjeta de débito ha sido desbloqueada'
        if tipo == 'credito':
            ejecutarSentencia2('desbloquearTarjeta', 'Credito', currentUser['id'])
            mensaje = 'Su tarjeta de crédito ha sido desbloqueada'

    return mensaje 


def bloqueoDesbloqueoTarjetaP1(update: Update, context: CallbackContext):
    mensaje = '1. Débito \n 2. Crédito \n \n Escriba el tipo de tarjeta'
    update.message.reply_text(mensaje)
    return tarjetaP2



def bloqueoDesbloqueoTarjetaP2(update: Update, context: CallbackContext):
    global tipoTarjeta 
    tipoTarjeta = update.message.text
    dato = ejecutarSentencia('comprobarTarjeta',currentUser['id'])
    if dato[0][0] is not None:
        correo.send_email(currentUser['correo'],currentUser['token'])
        return bloqueoDesbloqueoTarjeta3(update,context)

def bloqueoDesbloqueoTarjeta3(update: Update, context: CallbackContext):
    update.message.reply_text('Escribe el código de verficación enviado a tu correo electronico')
    return tarjetaP4

def bloqueoDesbloqueoTarjeta4(update: Update, context: CallbackContext):
    global mensajeTarjeta
    codigo = update.message.text
    print(codigo,estadoTarjeta,tipoTarjeta)
    if codigo == currentUser['token']:
        mensajeTarjeta = bloquearDesbloquear(estadoTarjeta,tipoTarjeta)
        return bloqueoDesbloqueoTarjetaP5(update,context)
    
def bloqueoDesbloqueoTarjetaP5(update: Update, context: CallbackContext):
    global mensajeTarjeta
    update.message.reply_text(mensajeTarjeta)
        

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2072414162:AAHuEcnXbkKTCUucD0wRFy3l7bVkT08PiPs")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            estadologin: [MessageHandler(Filters.text, loginP1)],
            estadologinP1: [MessageHandler(Filters.text, loginP2)],
            estadologinP2: [MessageHandler(Filters.text, loginP3)],
            estadoMenuP1: [MessageHandler(Filters.text, menuP1)],
            agendarCitaP4:[MessageHandler(Filters.text, citaP4)],
            agendarCitaP6:[MessageHandler(Filters.text,citaP6)],
            tarjetaP2:[MessageHandler(Filters.text, bloqueoDesbloqueoTarjetaP2)],
            tarjetaP4:[MessageHandler(Filters.text, bloqueoDesbloqueoTarjeta4)],
            analisisSentimiento:[MessageHandler(Filters.text,analisiSentimientosP2)]
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    print("BOT IS RUNNING")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


main()
