#Asignador de talleres recreativos EPJ 2023
#Programado por Benjamín Santelices.
import mysql.connector
import random

SQL = mysql.connector.connect(host="host", user="user", passwd="pass", db="control_epj") #conectar a base de datos SQL.
SQLc = SQL.cursor()

cmd = "SELECT correlativo FROM respuestas_talleres" #obtener correlativos de respuestas de inscripción a talleres.
SQLc.execute(cmd)
talleres = [x[0] for x in SQLc.fetchall()] #convertir tupla de tuplas en lista de listas.

cmd = "SELECT buses.correlativo FROM buses JOIN inscripciones ON buses.correlativo = inscripciones.correlativo  WHERE buses.libreta = 1 and inscripciones.grupo != 0" #buscar personas que no sean asesores (grupo != 0) hayan llegado (libreta = 1)
SQLc.execute(cmd) 
libretas = [x[0] for x in SQLc.fetchall()] #convertir tupla de tuplas en lista de listas.

for l in libretas: #buscar gente que haya venido pero no se ha inscrito.
    if l not in talleres: #si no está, elegir preferencias al azar.
        choice = list(range(1,9)) #generar vector de preferencias.
        random.shuffle(choice) #generar vector aleatorio.
        cmd = f"INSERT INTO respuestas_talleres (correlativo, futbol, basquetbol, voleibol, juegos_mesa, fitfolk, pausa_activa, yoga, taekwondo) VALUES ({l},{choice[0]},{choice[1]},{choice[2]},{choice[3]},{choice[4]},{choice[5]},{choice[6]},{choice[7]})" #agregar opción a respuestas.
        print(cmd)
        SQLc.execute(cmd)
        SQL.commit()

cupos = {}
cmd = "SELECT * FROM cupos_talleres" #seleccionar nómina de cupos.
SQLc.execute(cmd)
for x in SQLc.fetchall(): #generar diccionario donde la llave es el taller y el valor la cantidad de cupos.
    cupos[x[0]] = x[1]
talleres = list(cupos.keys()) #hacer lista de talleres.
print(talleres)


cmd = "SELECT * FROM respuestas_talleres" #obtener respuestas de todos los participantes.
SQLc.execute(cmd)
data = [list(x) for x in SQLc.fetchall()] #convertir tupla de tuplas en lista de listas.
for i in data: #iterar por participante.
    print(i[0])
    for j in range(1,9): #iterar por preferencia, si la primera opción no tiene cupo pasa a la siguiente.
        print(j)
        indice = i.index(j) - 2 #obtener columna correspondiente al taller respecto a la decisión.
        esteTaller = talleres[indice]
        if cupos[esteTaller] != 0: #si quedan cupos en el taller, agregar, si no continuar.
            cupos[esteTaller] -= 1 #quitar cupo al taller.
            cmd = f"UPDATE respuestas_talleres SET taller = \"{esteTaller}\" WHERE correlativo = {i[0]}" #agregar a la tabla de inscripciones por correlativo.
            print(cmd)
            SQLc.execute(cmd)
            SQL.commit() #commit los datos.
            break #salir del bucle de preferencia, continuar con siguiente participante.