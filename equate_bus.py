#copiar buses a datos de inscripción para las etiquetas.
#Programado por Benjamín Santelices

#se que hay una forma más inteligente para hacer esto en una base de datos relacional, pero no se como y no tenía tiempo de aprender.

import mysql.connector

SQL = mysql.connector.connect(host="host", user="user", passwd="pass", db="control_epj") #conectar a base de datos SQL.
SQLc = SQL.cursor()

cmd = "SELECT id, bus FROM nombres_comunidades;" #obtener número de bus de la tabla de grupos.
SQLc.execute(cmd)
data = [list(x) for x in SQLc.fetchall()] #convertir tupla de tuplas en lista de listas.

buses = {} #llave es el número del bus, grupo corresponde a los grupos que van arriba.
for grupo in data:
    buses[grupo[0]] = grupo[1] #poblar diccionario.

for b in buses: #iterar sobre cada bus.
    cmd = f"UPDATE inscripciones SET bus = {buses[b]} WHERE grupo = {b}" #agregar ID de bus a participantes de cada grupo.
    SQLc.execute(cmd)
SQL.commit()