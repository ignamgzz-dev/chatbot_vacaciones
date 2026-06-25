import csv
import os

# archivo que funciona como base de datos
ARCHIVO = "empleados.csv"

def inicializar_bd():
    if not os.path.exists(ARCHIVO):
        with open(ARCHIVO, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['nombre', 'dias_disponibles'])
            # empleados de prueba
            writer.writerow(['Juan Perez', 15])
            writer.writerow(['Maria Lopez', 8])
            writer.writerow(['Carlos Garcia', 0])

def buscar_empleado(nombre):
    with open(ARCHIVO, 'r') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            if fila['nombre'].lower() == nombre.lower():
                return fila
    return None

def actualizar_dias(nombre, dias_nuevos):
    filas = []
    with open(ARCHIVO, 'r') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            if fila['nombre'].lower() == nombre.lower():
                fila['dias_disponibles'] = dias_nuevos
            filas.append(fila)
    with open(ARCHIVO, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['nombre', 'dias_disponibles'])
        writer.writeheader()
        writer.writerows(filas)

def chatbot():
    inicializar_bd()
    print("Bienvenido al sistema de vacaciones")
    print("-------------------------------------")

    nombre = input("Bot: ingresa tu nombre completo: ").strip()
    
    # valido que no este vacio
    if nombre == "":
        print("Bot: tenes que ingresar un nombre")
        return

    empleado = buscar_empleado(nombre)
    
    if empleado == None:
        print("Bot: no te encontre en el sistema, fijate si escribiste bien tu nombre")
        return

    print(f"Bot: hola {empleado['nombre']}! tenes {empleado['dias_disponibles']} dias disponibles")

    # pido los dias que quiere solicitar
    try:
        dias = int(input("Bot: cuantos dias queres solicitar? "))
        if dias <= 0:
            print("Bot: tiene que ser un numero mayor a cero")
            return
    except ValueError:
        print("Bot: eso no es un numero valido, tenes que escribir un numero entero")
        return

    # verifico si tiene saldo suficiente
    if int(empleado['dias_disponibles']) >= dias:
        dias_restantes = int(empleado['dias_disponibles']) - dias
        actualizar_dias(nombre, dias_restantes)
        print(f"Bot: solicitud aprobada! se descontaron {dias} dias")
        print(f"Bot: te quedan {dias_restantes} dias disponibles")
    else:
        print("Bot: solicitud rechazada, no tenes suficientes dias")
        print(f"Bot: solo tenes {empleado['dias_disponibles']} dias disponibles")

    # pregunto si quiere hacer otra solicitud
    otra = input("Bot: queres hacer otra solicitud? (si/no) ").strip().lower()
    if otra == "si":
        chatbot()
    else:
        print("Bot: hasta luego!")

chatbot()