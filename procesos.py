import correo
import DB_utility
import random
conexion=DB_utility.DBConnector()


currentUser = {}
diasDisponibles=[]
horasDisponibles=[]

def login():
    global currentUser
    print('Hola necesito tu Cedula de identidad.')
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