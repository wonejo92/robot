import DB_utility
import correo

conexion = DB_utility.DBConnector()


def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ('hello'):
        return 'Hola que tal'

    if user_message in ('de donde eres ?'):
        return 'Ecuador'

    if user_message in ('y que haces ?'):
        return 'nada'

    return 'No entiendo'


bandera = bool


def inicioBot(input_text):
    global bandera
    global currentUser
    user_message = str(input_text).lower()
    if user_message == '1':
        return 'Hola necesito tu Cedula de identidad.'
    currentUser = obtenerDatos(input_text)
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
