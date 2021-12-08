import DB_utility

conexion=DB_utility.DBConnector()


def funca():
    print(conexion.execute_query(conexion.sql_dict.get('obtener'),()))



funca()
