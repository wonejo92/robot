import correo
import DB_utility
import random

valor=str
conexion=DB_utility.DBConnector()


currentUser = {}
diasDisponibles=[]
horasDisponibles=[]

def login():
    global currentUser
    cedula= input()
    user=conexion.execute_query(conexion.sql_dict.get('getClient'),(cedula,))
    id=user[0][0]
    nombres = user[0][2]
    apellidos = user[0][3]
    email=user[0][4]
    token=user[0][5]

    correo.send_email(email,token)
    print('\n')
    print('Ingresa el codigo de verificacion'
          'que se envio a tu correo electronico !!')
    codigo=input()
    if(codigo==token):
        currentUser={"id": id, "cedula": cedula, "nombres": nombres, "apellidos": apellidos, "correo": email, "token": token }
        return True

    else:
        return False


def Agendar_Cita():
    global diasDisponibles
    global horasDisponibles
    #print("\n")
    print("Para el proceso de apertura de una cuenta procederemos a agendarte una cita \n"
          "Horarios Disponibles !!")
    horario=conexion.execute_query(conexion.sql_dict.get("getSchedule"),())
    for i in range(len(horario)):
        diasDisponibles.append(horario[i][0])
    for j in range(len(diasDisponibles)):
        print(j + 1,' : ', diasDisponibles[j])
    print("Ingresa el dia que necesites la cita")
    numDia=int(input())
    dia=diasDisponibles[numDia - 1]

    horas=conexion.execute_query(conexion.sql_dict.get("getHourSchedule"),(dia,))
    for h in range(len(horas)):
        horasDisponibles.append(horas[h][0])
    print("Horas disponibles. ")
    for k in range(len(horasDisponibles)):
        print(k + 1, ' : ', horasDisponibles[k])
    print('\n')
    print("Ingresa la hora que necesites")
    numhora=int(input())
    hora= horasDisponibles[numhora - 1]

    # Se obtiene el id de la cita
    consultaId=conexion.execute_query(conexion.sql_dict.get("getIdSchedule"),(dia,hora))
    idhora=consultaId[0][0]

    print("Todo listo la cita se agendara a nombre de :",currentUser['nombres'] , currentUser['apellidos'])
    # Se procede a separa un horario
    conexion.execute_query(conexion.sql_dict.get("defineSchedule"),(idhora,))
    conexion.execute_query('commit', None)

    #Se procede a crear la cita
    codigoCita=random.randint(1000, 9999)
    conexion.execute_query(conexion.sql_dict.get("createAppointment"),(0,codigoCita,dia,hora,'SI',currentUser["id"],idhora))
    conexion.execute_query('commit', None)
    print("Genial tu cita esta agendada 😊"
          "Recuerda llegar 10 antes  con el siguiente codigo : \n"
          ,codigoCita)


def Consulta_Cuenta():
    print(currentUser)
    print("Para continuar con el proceso!! \n")
    print("Escribe el número de verificación que le hemos enviado a su correo electrónica ")
    account=conexion.execute_query(conexion.sql_dict.get("accountInquiry"),(currentUser["nombres"],))
    nombre=currentUser["nombres"]
    print("Bienvenido", nombre ," aquí están los datos de tu cuenta.\n")

    print("Numero de cuenta:",account[0][0],"\n"
          "Fecha de creacion:",account[0][1],"\n"
          "Monto en USD:",account[0][2],"\n"
          "Tipo :",account[0][3],"\n")

def obtenerMillas():
    numeroTarjeta = conexion.execute_query(conexion.sql_dict.get("obtenerIdTarjeta"),(currentUser['id'],))
    cantidadMillas = conexion.execute_query(conexion.sql_dict.get('obtenerMillas'),(numeroTarjeta[0][0],))
    print('Estimado cliente dispone de: ',cantidadMillas[0][0],' millas')
    print('Premios disponibles para canjear: ')
    #print(type(cantidadMillas[0][0]))
    premiosCanjeables(int(cantidadMillas[0][0]))

def premiosCanjeables(cantidadDeMillas):
    if cantidadDeMillas < 89 :
        print('No cuentas actualmente con premios canjeables')
    if cantidadDeMillas <= 100 and cantidadDeMillas >= 90:
        print('Felicidades ! acabas de ganar una orden de consumo de:' ,'\n')
        print('20.00 dolares en Pizza Hut, presentate en el establecimiento para','\n')
        print('reclamar el premio')
    if cantidadDeMillas <= 500 and cantidadDeMillas >= 300:
        print('Felicidades ! acabas de ganar un noche gratis en el hostal','\n',
              'Rancho Dorado, acercate al hostal para reclamar tu premio')
    if cantidadDeMillas <= 5000 and cantidadDeMillas >= 4000:
        print('Felicidades ! acabas de ganar un vuelo a Costa Rica de ida y vuelta','\n',
              'ponte en contacto con nosotros para darte mas información')

def ejecutarSentencia(sentencia,parametro):
    dato = conexion.execute_query(conexion.sql_dict.get(sentencia),(parametro,))
    return dato

def ejecutarSentencia2(sentencia,parametro,parametro2):
    conexion.execute_query(conexion.sql_dict.get(sentencia), (parametro, parametro2,))
    conexion.execute_query('commit', None)

def bloqueoDesbloqueoTarjeta(estado):
    print("1. Debito",'\n')
    print('2. Credito','\n')
    print("Escriba el tipo de tarjeta")
    tipo = int(input())
    dato = ejecutarSentencia('comprobarTarjeta',currentUser['id'])
    if dato[0][0] is not None:
        print('Escribe el código de verficación enviado a tu correo electronico')
        codigo = input()
        correo.send_email(currentUser['correo'],currentUser['token'])
        if codigo == currentUser['token']:
            if estado == 'bloquear':
                if tipo == 1:
                    ejecutarSentencia2('bloquearTarjeta', 'Debito', currentUser['id'])
                    print('Su tarjeta ha sido bloqueada')
                if tipo == 2:
                    ejecutarSentencia2('bloquearTarjeta', 'Credito', currentUser['id'])
                    print('Su tarjeta ha sido bloqueada')
            if estado == 'desbloquear':
                if tipo == 1:
                    ejecutarSentencia2('desbloquearTarjeta', 'Debito', currentUser['id'])
                    print('Su tarjeta ha sido desbloqueada')
                if tipo == 2:
                    ejecutarSentencia2('desbloquearTarjeta', 'Credito', currentUser['id'])
                    print('Su tarjeta ha sido desbloqueada')
    else:
        print('no se encontraron coincidencias')

def Consultas_Generales():
    print('funciona')






