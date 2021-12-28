import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Updater,CommandHandler,MessageHandler,Filters,ConversationHandler,CallbackContext,
)
import correo
import DB_utility
conexion=DB_utility.DBConnector()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(_name_)
#Estados
estadologin=0
estadologinP1=0.1
estadologinP2=0.2
estadomenu=1
#Variables
user={}
currentUser = {}


GENDER, PHOTO, LOCATION, BIO = range(4)

def start(update: Update, context: CallbackContext) :
    """Starts the conversation and asks the user about their gender."""
    update.message.reply_text('Hola soy CORA 😉, tu asistente virtual !! \n\n '
                              '¿ Tienes cuenta con nosotros ? \n  SI \n  NO \n')
    return estadologin


def bio(update: Update, context: CallbackContext) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

"""Funciones para el logeo del cliente"""

def loginP1(update: Update, context: CallbackContext):
    text=update.message.text
    if(text=='si'):
        update.message.reply_text('Ingresa tu Numero de Cedula !')
        return estadologinP1
    else:
        update.message.reply_text('Procederemos a agendarte una cita para crearte una cuenta.')

def loginP2(update: Update, context: CallbackContext):
    global user
    cedula = update.message.text
    print("Mensaje en loginp2",cedula)
    user = conexion.execute_query(conexion.sql_dict.get('getClient'), (cedula,))
    email=user[0][4]
    token=user[0][5]
    correo.send_email(email,token)
    update.message.reply_text('Ingresa el codigo que se te envio al correo Electronico registrado !')
    return estadologinP2

def loginP3(update: Update, context: CallbackContext):
    global user
    global currentUser
    codigo = update.message.text
    id=user[0][0]
    cedula=user[0][1]
    nombres = user[0][2]
    apellidos = user[0][3]
    email=user[0][4]
    token=user[0][5]
    if(codigo==token):
        print("Persona Verificada")
        currentUser = {"id": id, "cedula": cedula, "nombres": nombres, "apellidos": apellidos, "correo": email,
                       "token": token}
        print(currentUser)
        menu(update,context)
        return estadomenu
    else:
        print("Paso algun error")

def menu(update: Update, context: CallbackContext):
    print("Llamando al menu")
    update.message.reply_text("Se procede a mostrar el menu")

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2032337510:AAHV9z41Q4WvXS3J3xUVF6d-HJUnw0-f4eM")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            estadologin:[MessageHandler(Filters.text,loginP1)],
            estadologinP1:[MessageHandler(Filters.text,loginP2)],
            estadologinP2:[MessageHandler(Filters.text,loginP3)],
            estadomenu:[MessageHandler(Filters.text,menu)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    print("BOT IS RUNNING")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if _name_ == '_inicio_':
    main()