import mysql.connector

def conectar():

    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="construdata"
    )

    return conexion