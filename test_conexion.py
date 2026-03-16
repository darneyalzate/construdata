from conexion import conectar

db = conectar()

print("Conexion exitosa")

db.close()