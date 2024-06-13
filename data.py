#Imprimir datos del participante EPJ 2023.
#Programado por Benjamín Santelices
import mysql.connector

SQL = mysql.connector.connect(host="host", user="user", passwd="pass", db="control_epj") #conectar a la base de datos SQL.
SQLc = SQL.cursor()

while True: #repetir infinitamente bucle de datos.
    corr = input("\nCorrelativo: ") #entrada de correlativo por pistola o manual.
    cmd = f"SELECT * FROM inscripciones WHERE correlativo = {corr}" #obtener datos de la base de datos.
    SQLc.execute(cmd)
    data = SQLc.fetchall()[0] #obtener primer resultado (debiese ser sólo uno)

    #imprimir datos del participante.
    print("Nombre: ", data[1])
    print("Obra: ", data[3])
    print("Grupo: ", data[8])
    print("Bus: ", data[9])
