import DB_utility
import procesos

conexion=DB_utility.DBConnector()

def initialMessage():
    print('Hola soy CORA 😉, tu asistente virtual !! \n\n'
          '¿ Tienes cuenta con nosotros ? \n'
          '1 : SI \n'
          '2 : NO \n')
    answer= eval(input())

    if(answer==1):
        #print('Tiene cuenta')
        print('\n')
        result=procesos.login()
        print(result)
       # showMenu()
    else:
        print('No tiene cuenta')


def showMenu():
    print('¿ Como te ayudo ? \n\n'
          '1. Agendar una cita \n'
          '2. Consulta de cuenta \n'
          '3. Consulta de millas \n'
          '4. Bloqueo de Tarjetas \n'
          '5 Desbloqueo de tarjetas \n'
          '6 Consultas Generales \n'
          '7 Dejar un comentario \n')

initialMessage()
