import mysql.connector

try:

    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="construdata"
    )

    print("Conexion exitosa")

except Exception as e:

    print("Error:",e)