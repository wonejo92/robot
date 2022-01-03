# Library for connecting to the database.
import mysql.connector


class DBConnector:

    # Dict containing SQL queries related to database.
    sql_dict = {
        'getClient': 'select * from cliente where cedula = %s',
        'getSchedule': 'select dia_semana from horario where disponibilidad='+"'Disponible'"+ 'group by dia_semana',
        'getHourSchedule': 'select hora from horario where disponibilidad='+"'Disponible'"+ ' and dia_semana= %s',
        'getIdSchedule': 'select idHorario from horario where dia_semana= %s and hora= %s',
        'defineSchedule': ' update horario set disponibilidad='+"'Ocupado'"+ ' where idHorario= %s',
        'createAppointment': 'insert into cita values (%s, %s, %s, %s, %s, %s,%s )',

        'accountInquiry': 'select numeroDeCuenta, fechaCreacion, monto, tipo from cuenta cu, cliente cli'
                          ' where cu.Cliente_idCliente = cli.idCliente and cli.nombres= %s',

        'obtenerIdTarjeta': 'select idTarjeta from tarjeta where Cliente_idCliente = %s',
        'obtenerMillas': 'select cantidadMillas from millas where Tarjeta_idTarjeta = %s',
        'comprobarTarjeta': 'select numeroTarjeta from tarjeta where Cliente_idCliente = %s',
        'bloquearTarjeta': "UPDATE tarjeta SET estado='Inactiva' where tipoTarjeta = %s and Cliente_idCliente = %s",
        'desbloquearTarjeta': "UPDATE tarjeta SET estado='Activa' where tipoTarjeta = %s and Cliente_idCliente = %s",
        'buscar_usuario': 'select cedula from CLIENTE'
    }

    # Dict containing Error/Message codes related to SQL returns.
    messages_dict = {
        0: 'Se realizo la transferencia correctamente',
        -1: 'No tiene saldo suficiente para hacer la transferencia',
        -2: 'La institucion no existe o es incorrecta',
        -3: 'La cuenta financiera no existe en base al numero de cuenta o a la institucion'
    }

    def __init__(self):
        """
        Class constructor.
        Creates a new instance of mysql connector using connection parameters.
        """
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='chatbot',
            auth_plugin='mysql_native_password'
        )

    def execute_query(self, sql_query: str, parameters: tuple):
        """
        Method for executing a query with or without parameters.
        :param sql_query: A valid SQL query based on sql_dict.
        :param parameters: A tuple which contains information related to sql_query.
        :return: a list of results containing information.
        """
        cursor = self.db.cursor()
        if parameters is not None:
            #print(sql_query, '___', parameters)
            cursor.execute(sql_query, parameters)
            return cursor.fetchall()
        else:
            cursor.execute(sql_query)
            return cursor.fetchall()
