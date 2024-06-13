#Asignador de charlas EPJ 2023
#Programado por Benjamín Santelices

import mysql.connector
import random

SQL = mysql.connector.connect(host="host", user="user", passwd="pass", db="control_epj") #conectar a base de datos SQL.
SQLc = SQL.cursor()

cmd = "SELECT correlativo FROM respuestas_charlas" #cargar solo correlativos de tabla (gente que se inscribió).
SQLc.execute(cmd)
talleres = [x[0] for x in SQLc.fetchall()] #convertir tupla de tuplas en lista de listas.

cmd = "SELECT buses.correlativo FROM buses JOIN inscripciones ON buses.correlativo = inscripciones.correlativo WHERE buses.libreta = 1 and inscripciones.grupo != 0" #buscar personas que no sean asesores (grupo != 0) hayan llegado (libreta = 1)
SQLc.execute(cmd)
libretas = [x[0] for x in SQLc.fetchall()] #convertir tupla de tuplas en lista de listas.

for l in libretas: #iterar por cada participante.
    if l not in talleres: #si participante no se inscribió, ingresar valores de preferencia al azar.
        choice = list(range(1,8)) #crear vector de preferencias.
        random.shuffle(choice) #mezclar vector de preferencias para obtener valores aleatorios.
        cmd = f"INSERT INTO respuestas_charlas (correlativo, mati, natacha, berni, erich, rodrigo, rene, jota) VALUES ({l},{choice[0]},{choice[1]},{choice[2]},{choice[3]},{choice[4]},{choice[5]},{choice[6]})" #cargar valores aleatorios a la lista.
        print(cmd)
        SQLc.execute(cmd)
        SQL.commit()

cupos = {}
cmd = "SELECT * FROM cupos_charlas" #cargar la nómina de cupos de cada charla.
SQLc.execute(cmd)
for x in SQLc.fetchall(): #convertir tabla en diccionario, donde la llave es la charla y el valor es el cupo.
    cupos[x[0]] = x[1]
talleres = list(cupos.keys())
print(talleres) #imprimir lista de cupos para asegurar que esté bien.


cmd = "SELECT * FROM respuestas_charlas" #cargar respuestas de inscripciones de participantes.
SQLc.execute(cmd)
data = [list(x) for x in SQLc.fetchall()] #pasar de tupla de tuplas a lista de listas.
for i in data: #iterar sobre cada participante.
    print(i[0])
    for j in range(1,9): #iterar sobre cada preferencia, de mayor a menor.
        print(j)
        indice = i.index(j) - 2 #obtener la columna que tiene la preferencia de la iteración actual.
        esteTaller = talleres[indice] #obtener nombre de charla correspondiente a la columna.
        if cupos[esteTaller] != 0: #si quedan cupos en la charla, asignar a participante. Si no, continúa a la opción siguiente.
            cupos[esteTaller] -= 1 #quitar cupo de la charla elegida.
            cmd = f"UPDATE respuestas_charlas SET charla = \"{esteTaller}\" WHERE correlativo = {i[0]}" #cargar preferencia a respuestas.
            print(cmd)
            SQLc.execute(cmd)
            SQL.commit()
            break #salir del for de preferencias, continúa al siguiente participante.