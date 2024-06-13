#Asignador de grupos EPJ 2023.
#Programado por Benjamín Santelices.

import mysql.connector
import datetime

def listaDeObras(SQLc): #obtiene la lista de grupos y genera el diccionario de coeficientes para ordenar de más grande a más pequeño.
    cmd = "SELECT DISTINCT obra, zona, COUNT(correlativo) FROM inscripciones WHERE modalidad = \"Participante\" GROUP BY obra, zona;"
    SQLc.execute(cmd)
    tableObras = SQLc.fetchall()
    tableObras = [list(x) for x in tableObras] #obtener lista de listas de todas las obras con sus respectivas zonas y números.

    cmd = "SELECT DISTINCT zona, COUNT(correlativo) FROM inscripciones WHERE modalidad = \"Participante\" GROUP BY zona;"
    SQLc.execute(cmd)
    tableZonas = SQLc.fetchall()
    tableZonas = [list(x) for x in tableZonas] #obtenert lista de listas de todas las zonas con sus números

    cmd = "SELECT DISTINCT COUNT(correlativo) FROM inscripciones WHERE modalidad = \"Participante\";"
    SQLc.execute(cmd)
    total = SQLc.fetchall()[0][0] #obtener total de participantes

    dictObras = {}
    for obra in tableObras:
        dictObras[obra[0]] = (obra[2] / total) #obtener multiplicador para cada obra respecto del total

    dictZonas = {}
    for zona in tableZonas:
        dictZonas[zona[0]] = (zona[1] / total) #obtener multiplicador para cada zona respecto del total

    dictCoefs = {}
    for obra in tableObras:
        dictCoefs[obra[0]] = dictObras[obra[0]] * dictZonas[obra[1]] #obtener coeficiente multiplicando ambos diccionarios y reemplazar número por coeficiente.

    return dictCoefs

def hacerGrupos(dictFreq, SQLc): #crear grupos
    cmd = "SELECT correlativo, sexo, obra, fecha_nacimiento FROM inscripciones WHERE modalidad = \"Participante\";"
    SQLc.execute(cmd)
    data = SQLc.fetchall()
    data = [list(x) for x in data] #obtener lista completa de participantes

    for item in data:
        item.append(dictFreq[item[2]]) #agregar coeficiente de obra
        if item[3] == None:
            item[3] = datetime.date(2010, 1, 1)
        
    data.sort(key=lambda x: (x[4], x[1], x[3])) #ordenar en función de coeficiente, sexo, fecha de nacimiento, en ese orden.

    cmd = "SELECT id, cantidad FROM nombres_comunidades;"
    SQLc.execute(cmd)
    comunidades = SQLc.fetchall()
    comunidades = [list(x) for x in comunidades] #obtener disposición de los grupos.

    grupos = {}
    for cmn in comunidades:
        grupos[cmn[0]] = [None for i in range(cmn[1])] #generar grupos con None como placeholder para cada persona. La llave es el número de grupo.

    counter = 1
    for item in data: #iterar sobre usuarios para asignar a grupos
        if None in grupos[counter]:
            grupos[counter][grupos[counter].index(None)] = item[0]  #asignar usuario al grupo, cambias el primer None que encuentra.
    
        counter += 1
        if counter > len(grupos): #si el contador supera el número de grupos, hacer rollover.
            counter = 1

    for i in grupos:
        while None in grupos[i]:
            grupos[i].pop(grupos[i].index(None)) #quitar los None que sobren.

    return grupos
    
def printGrupos(grupos): #imprime todos los grupos en un formato legible.
    total = 0 #para imprimir total de grupos, cada iteración aumenta el tamaño.
    for i in grupos:
        print(f"\nGRUPO {i}")
        print(grupos[i])
        total += len(grupos[i])
    
    print(f"\nTOTAL: {total}")

def appendGruposSQL(SQL, SQLc, grupos): #añadir ID de grupo a cada participante.
    ids = grupos.keys() #obtener todos los grupos.
    for i in ids: #iterar por cada grupo
        for correlativo in grupos[i]: #iterar por cada participante dentro de cada grupo.
            cmd = f"UPDATE inscripciones SET grupo = {i} WHERE correlativo = {correlativo};" #subir a la base a nueva columna.
            SQLc.execute(cmd)
    SQL.commit()


#main
print("Creador de grupos EPJ SSCC 2023")
print("Creado por Benjamin Santelices")
print("Conectando a Servidor SQL...")

SQL = mysql.connector.connect(host="host", user="user", passwd="pass", db="control_epj")
SQLc = SQL.cursor()
print("Conectado! Comenzando script...")

print("Calculando coeficientes de tamaño por obra...")
freq = listaDeObras(SQLc)

print("Generando grupos...")
grupos = hacerGrupos(freq, SQLc)

printGrupos(grupos)
appendGruposSQL(SQL, SQLc, grupos)