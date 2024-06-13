#Sincronizar correlativos entre tablas de inscripciones, buses, y almuerzos.
#Programado por Benjamín Santelices.

#se que hay una forma más inteligente para hacer esto en una base de datos relacional, pero no se como y no tenía tiempo de aprender.

import mysql.connector

SQL = mysql.connector.connect(host="host", user="user", passwd="pass", db="control_epj") #conectar a base de datos SQL.
SQLc = SQL.cursor()

cmd = "SELECT correlativo FROM inscripciones;" #obtener correlativos de base de datos de inscripciones.
SQLc.execute(cmd)
insc = SQLc.fetchall()
insc = [x[0] for x in insc] #convertir tupla de tuplas en lista de listas.
print(len(insc))

cmd = "SELECT correlativo FROM buses;" #obtener correlativos ya presentes en tabla buses.
SQLc.execute(cmd)
buses = SQLc.fetchall()
buses = [x[0] for x in buses] #convertir tupla de tuplas en lista de listas.
print(len(buses))

cmd = "SELECT correlativo FROM almuerzos;" #obtener correlativos ya presentes en tabla almuerzos.
SQLc.execute(cmd)
almz = SQLc.fetchall()
almz = [x[0] for x in almz] #convertir tupla de tuplas en lista de listas.
print(len(almz))


for corr in insc: #iterar sobre correlativos de inscripciones
    if corr not in almz: #si correlativo no está en almuerzo, agregar.
        print("Almuerzo: ", corr)
        cmd = f"INSERT INTO almuerzos (correlativo) VALUES ({corr});"
        SQLc.execute(cmd)

    if corr not in buses: #si correlativo no está en buses, agregar.
        print("Buses", corr)
        cmd = f"INSERT INTO buses (correlativo) VALUES ({corr});"
        SQLc.execute(cmd)




SQL.commit() #commit a tablas.