#Ingestor de buses, libretas, y polera.
import mysql.connector

SQL = mysql.connector.connect(host="host", user="user", passwd="pass", db="control_epj") #conectar a la base de datos SQL.
SQLc = SQL.cursor()

print("---CONTROL DE BUSES Y LIBRETAS---")

columns = ["ida", "vuelta", "libreta", "polera"] #columnas en la tabla de control.

print("Seleccione el viaje a controlar escribiendo su número:")
print("0. Ida") #bus ida
print("1. Vuelta") #bus vuelta
print("2. Libreta") #recibió libreta
print("3. Polera") #recibió polera

choice = int(input("Viaje: ")) #recibir entrada
assert choice in range(4) #confirmar que entrada esté dentro del rango entregado.
choice = columns[choice] #obtener columna a manipular.


while True:
    corr = input("\nCorrelativo: ") #recibir correlativo de pistola o manualmente.
    cmd = f"SELECT * FROM inscripciones WHERE correlativo = {corr}" #obtener datos del participante.
    SQLc.execute(cmd)
    data = SQLc.fetchall()
    if len(data) != 1: #si no es reconocido el correlativo, lanzar error y continuar.
        print("ERROR: Correlativo no reconocido.")
        continue

    data = data[0] #si se reconoce, imprimir datos del participante.
    print("Nombre: ", data[1])
    print("Obra: ", data[3])
    print("Grupo: ", data[8])
    print("Bus: ", data[9])

    cmd = (f"SELECT correlativo, {choice} FROM buses WHERE correlativo = {corr}") #buscare datos de la tabla de control.
    SQLc.execute(cmd)
    almuerzo = SQLc.fetchall()[0]
    print(almuerzo)
    if almuerzo[1] == 0: #si persona existe y no registra lo buscado, agregar un 1 y continuar.
        print("Viaje registrado!")
        cmd = f"UPDATE buses SET {choice} = 1 WHERE correlativo = {corr}"
        SQLc.execute(cmd)
        SQL.commit()
    else: #si la persona existe y ya registra lo buscado, lanzar error y continuar.
        print("ERROR: Persona ya viajó!")
