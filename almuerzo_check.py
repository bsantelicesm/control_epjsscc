#Ingestor de almuerzos EPJ 2023
#Desarrollado por Benjamín Santelices

import mysql.connector

SQL = mysql.connector.connect(host="host", user="user", passwd="pass", db="control_epj")
SQLc = SQL.cursor() #conectar a base de datos SQL.

#Imprimir interfaz de selección de día.
print("---CONTROL DE ALMUERZOS---")

columns = ["comida26", "desayuno27", "almuerzo27", "comida27", "desayuno28", "almuerzo28", "comida28", "desayuno29", "almuerzo29", "comida29", "desayuno30"] #nombre de las columnas en la tabla.

print("Seleccione la comida a controlar escribiendo su número:")

#número asociado a cada comida corresponde al indice en la lista columns.
print("0. Comida 26")
print("1. Desayuno 27 | 2. Almuerzo 27 | 3. Comida 27")
print("4. Desayuno 28 | 5. Almuerzo 28 | 6. Comida 28")
print("7. Desayuno 29 | 8. Almuerzo 29 | 9. Comida 29")
print("10. Desayuno 30\n")


choice = int(input("Comida: ")) #pedir entrada.
assert choice in range(11) #confirmar que la entrada sea dentro de los valores pedidos.
choice = columns[choice] #obtener nombre de columna.
print(choice)


while True: #repetir infinitamente, cada bucle es una persona controlada.
    corr = input("\nCorrelativo: ") #elegir correlativo, toma de las pistolas o manualmente.
    cmd = f"SELECT * FROM inscripciones WHERE correlativo = {corr}" #obtener info de participante de base de datos.
    SQLc.execute(cmd)
    data = SQLc.fetchall()
    if len(data) != 1: #si no encuentra el correlativo en la base, imprimir error y comenzar de nuevo.
        print("ERROR: Correlativo no reconocido.")
        continue

    data = data[0] #si se encuentra la data imprimir información del participante.
    print("Nombre: ", data[1])
    print("Obra: ", data[3])
    print("Grupo: ", data[8])
    print("Dieta: ", data[6])

    cmd = (f"SELECT correlativo, {choice} FROM almuerzos WHERE correlativo = {corr}") #confirmar si la persona comió previamente o no.
    SQLc.execute(cmd)
    almuerzo = SQLc.fetchall()[0]
    if almuerzo[1] == 0: #si la entrada de la tabla marca 0, entonces no ha comido.
        print("Almuerzo registrado!")
        cmd = f"UPDATE almuerzos SET {choice} = 1 WHERE correlativo = {corr}" #registar almuerzo poniendo un 1 en la tabla.
        SQLc.execute(cmd)
        SQL.commit()
    else: #si la persona ya comió, lanzar error y continuar.
        print("ERROR: Persona ya almorzó!") 
