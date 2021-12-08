import correo
import DB_utility
conexion=DB_utility.DBConnector()

def login():
    print('Hola necesito tu Cedula de identidad.')
    cedula= input()
    user=conexion.execute_query(conexion.sql_dict.get('getClient'),(cedula,))
    email=user[0][4]
    token=user[0][5]
    print(email, token)
    correo.send_email(email,token)
    print('\n')
    print('Ingresa el codigo de verificacion'
          'que se envio a tu correo electronico !!')
    codigo=input()
    if(codigo==token):
        return True
    else:
        return False





