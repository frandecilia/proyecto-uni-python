# --<>----<>----<>----< Imports >----<>----<>----<>-- #

import numpy as np
import os
from Pila_functions import *
from Registers import *
from time import sleep
from datetime import date, datetime

# --<>----<>----<>----< Funciones >----<>----<>----<>-- #


# Para consola

def Limpiar_consola(tiempo):
    """
    Procedimiento práctico encargado de limpiar la consola tras el periodo de tiempo indicado
    
    :param tiempo: Tiempo en segundos antes de limpiar la consola
    :return: None
    """
    sleep(tiempo)
    os.system('cls')
    
    return None


def Mostrar_logo():
    print("##############################################################################\n"+
        "||                  ,--.  ,--.           ,--.           ,--.                  ||\n"+
        "||                  |  '--'  |  ,---.  ,-'  '-.  ,---.  |  |                  ||\n"+
        "||                  |  .--.  | | .-. | '-.  .-' | .-. : |  |                  ||\n"+
        "||                  |  |  |  | ' '-' '   |  |   \   --. |  |                  ||\n"+
        "||                  `--'  `--'  `---'    `--'    `----' `--'                  ||\n"+
        "||                                                                            ||\n"+
        "||   ,-----.          ,--. ,--.  ,---.                          ,--.          ||\n"+
        "||  '  .--./  ,--,--. |  | `--' /  .-'  ,---.  ,--.--. ,--,--,  `--'  ,--,--. ||\n"+
        "||  |  |     ' ,-.  | |  | ,--. |  `-, | .-. | |  .--' |      \ ,--. ' ,-.  | ||\n"+
        "||  '  '--'\ \ '-'  | |  | |  | |  .-' ' '-' ' |  |    |  ||  | |  | \ '-'  | ||\n"+
        "||   `-----'  `--`--' `--' `--' `--'    `---'  `--'    `--''--' `--'  `--`--' ||\n"+
        "##############################################################################")


def Menu_opciones(*opciones):
    cantidad_opciones = len(opciones)
    
    while True:
        print('###\t\tIngrese la opción a realizar\t\t###')
        
        for i, opcion in enumerate(opciones):
            print(f'# {i + 1}. {opcion}')
        
        try:
            res = int(input('# '))
        except ValueError:
            print('# Ingrese un número valido #')
            Limpiar_consola(1)
            continue
        
        if res > cantidad_opciones or res < 1:
            print('# Ingrese una opción válida #')
            Limpiar_consola(1)
            continue
        
        return res


def Mostrar_precios(precios, tipos):
    """
    Procedimiento encargado de mostrar los precios y tipos disponibles especificados

    :param precios: Registro con los precios de una determinada cosa
    :param tipos: Vector con cada tipo de una determinada cosa
    :return: None
    """
    
    print('#'*20)
    cantidad_tipos = len(tipos)
    for i in range(cantidad_tipos):
        tipo = tipos[i]
        precio = precios[tipo]
        print(f'# {tipo.capitalize()} : ${float(precio)}')
    print('#'*20)
    
    return None


# Cálculos varios

def Calcular_anios(fecha):
    hoy = datetime.now()
    anios = hoy.year - fecha.year
    
    yaCumplio = hoy.month > fecha.month
    cumpleHoy = hoy.month == fecha.month and hoy.day >= fecha.day
    
    if not yaCumplio and not cumpleHoy:
        anios -= 1
    
    return anios


def Es_mayor(fecha):
    fecha_nac = datetime(int(fecha['anio']), int(fecha['mes']), int(fecha['dia']))
    
    edad = Calcular_anios(fecha_nac)
    
    if edad < 18: return False
    
    return True


def Es_fecha_valida(anio, mes, dia):
    try:
        fecha = date(anio, mes, dia)
    except ValueError:
        return False
    
    return True


def Cantidad_habitaciones(cantidades):
    largo_vec = len(cantidades)
    cant = 0
    
    for i in range(largo_vec):
        cant += cantidades[i]
    return cant


def Determinar_indice_huespedes(vec_huespedes):
    filas_vec = len(vec_huespedes)
    colum_vec = len(vec_huespedes[0])
    
    for j in range(colum_vec):
        for i in range(filas_vec):
            indice_desocupado = int(vec_huespedes[i, j]['numHabitacion']) == 0
            if indice_desocupado:
                return i
    
    return None


def Buscar_huesped_por_dni(vec_huespedes, dni):
    cant_i = len(vec_huespedes)
    cant_j = len(vec_huespedes[0])
    
    for j in range(cant_j):
        for i in range(cant_i):
            if int(vec_huespedes[i, j]['dni']) == dni:
                return i, j


def Buscar_por_dni(pila, dni, tipo):
    cant = len(pila)
    
    b = 0
    pila_aux = []
    Crear_pila(pila_aux)
    
    for _ in range(cant):
        x, error = Desapilar_registro(pila, tipo)
        
        if error:
            break
        
        if int(x['dniACargo']) == dni:
            b = 1
            break
        
        Apilar(pila_aux, x)
        
    Volver_a_apilar_registros(pila, pila_aux, tipo)
    
    if b != 1:
        return False 
    
    return x


def Determinar_siguiente_tipo(tipos, tipo):
    largo_tipos = len(tipos)
    
    for i in range(largo_tipos):
        if str(tipos[i]) == tipo:
            break
    
    if not i < largo_tipos - 1:
        return False
    
    return tipos[i + 1]


# Funciones de disponibilidad

def Disponible_en_fechas(vec_hab, i, entrada, salida):
    anio_actual = datetime.now().year
    
    for indice_mes in range(int(entrada['mes']) - 1, 12):
        for dia in range(int(entrada['dia']) - 1, 31):
            
            if not Es_fecha_valida(anio_actual, indice_mes + 1, dia + 1):
                continue
            
            if indice_mes == int(entrada['mes']) - 1 and dia < int(entrada['dia']) - 1:
                continue
            
            if indice_mes == int(salida['mes']) - 1 and dia > int(salida['dia']) - 1:
                continue
            
            mes = Indice_a_mes(indice_mes)
            
            disponible = str(vec_hab[i]['diario'][mes][dia])
            
            if disponible != 'Disponible':
                return False
    
    return True


def Verificar_disponibilidad(vec_hab, tipo, entrada, salida):
    largo_vec = len(vec_hab)
    
    for i in range(largo_vec):
        esTipo = vec_hab[i]['tipo'] == tipo
        
        if not esTipo: continue
        
        habilitada = vec_hab[i]['habilitada']
        
        if not habilitada: continue
        
        if not Disponible_en_fechas(vec_hab, i, entrada, salida): continue

        return vec_hab[i]['numero']
    
    return False


def Buscar_hab_por_num(vec_hab, num):
    cant_i = len(vec_hab)
    
    for i in range(cant_i):
        if int(vec_hab[i]['numero']) == num:
            return i
    return False


def Buscar_menos_reservada(vec_hab, reservas, tipo):
    cant = len(reservas)
    
    cont_menor = 99999999
    num_menor = 0
    
    pila_aux = []
    analizadas = []
    Crear_pila(pila_aux)
    Crear_pila(analizadas)
    
    for i in range(cant):
        x, error = Desapilar_registro(reservas, Reserva)
        
        if error:
            break
        
        num = int(x['numHabitacion'])
        Apilar(analizadas, x)
        cont = 1
        
        for j in range(cant-1):
            x, error = Desapilar_registro(reservas, Reserva)
            
            if error:
                break
            
            if int(x['numHabitacion']) == num:
                cont += 1
            
            Apilar(pila_aux, x)
        
        index = Buscar_hab_por_num(vec_hab, num)
        
        if cont < cont_menor and str(vec_hab[index]['tipo'][0]) == tipo:
            cont_menor = cont
            num_menor = num
        
        Volver_a_apilar_registros(reservas, pila_aux, Reserva)
    
    Volver_a_apilar_registros(reservas, analizadas, Reserva)
    
    return num_menor


def Obtener_reservas_para_hoy(reservas):
    cant_reservas = len(reservas)
    
    pila_aux = []
    Crear_pila(pila_aux)
    
    para_hoy = []
    Crear_pila(para_hoy)
    
    for i in range(cant_reservas):
        x, error = Desapilar_registro(reservas, Reserva)
        
        if error: break
        
        fecha = x['entrada']
        entrada = datetime(int(fecha['anio']), int(fecha['mes']), int(fecha['dia']))
        hoy = datetime.now()
        diff = hoy - entrada 
        
        if diff.days == 0:
            Apilar(para_hoy, x)
        
        Apilar(pila_aux, x)
    
    Volver_a_apilar_registros(reservas, pila_aux, Reserva)
    return para_hoy


def Obtener_huespedes_por_hab(vec_huespedes, nHab):
    cant_i = len(vec_huespedes)
    cant_j = len(vec_huespedes[0])
    
    huespedes = []
    Crear_pila(huespedes)
    
    for j in range(cant_j):
        for i in range(cant_i):
            
            if int(vec_huespedes[i, j]['numHabitacion']) != nHab:
                continue
            
            Apilar_registro(huespedes, vec_huespedes[i, j])
    
    return huespedes


def Obtener_menores_y_responsable(huespedes, dniACargo):
    cant_huespedes = len(huespedes)
    
    menores = []
    Crear_pila(menores)
    
    for _ in range(cant_huespedes):
        x, error = Desapilar_registro(huespedes, Huesped)
        
        if int(x['dni']) == dniACargo:
            responsable = x
            continue
        
        if bool(x['esResponsable']):
            continue
        
        Apilar_registro(menores, x)
    
    return menores, responsable


def Obtener_reserva_hab_menor(reservas):
    cant_reservas = len(reservas)
    
    pila_aux = []
    Crear_pila(pila_aux)
    
    menor = 99999999
    for i in range(cant_reservas):
        x, error = Desapilar_registro(reservas, Reserva)
        
        if error: break
        
        if int(x['numHabitacion']) < menor:
            reserva = x
            menor = int(x['numHabitacion'])
        
        Apilar(pila_aux, x)
    
    # Apilar las otras reservas exceptuando la menor
    for i in range(cant_reservas):
        x, error = Desapilar_registro(reservas, Reserva)
        
        if error: break
        
        if int(x['dniACargo']) == int(reserva['dniACargo']):
            continue 
        
        Apilar(reservas, x)
    
    return reserva


def Obtener_servicios_por_hab(nhab, servicios):
    cant = len(servicios)
    
    pila_aux = []
    Crear_pila(pila_aux)
    
    servs_para_hoy = []
    Crear_pila(servs_para_hoy)
    
    for i in range(cant):
        x, error = Desapilar_registro(servicios, Servicio)
        
        if error: break
        
        if int(x['numHabitacion']) != nhab:
            Apilar_registro(pila_aux, x)
        
        Apilar_registro(servs_para_hoy, x)
    
    Volver_a_apilar_registros(servicios, pila_aux, Servicio)
    return servs_para_hoy


def Obtener_reservas_vencidas(reservas):
    cant = len(reservas)
    
    pila_aux = []
    Crear_pila(pila_aux)
    
    purgadas = []
    Crear_pila(purgadas)
    
    cont = 0
    hoy = datetime.now()
    
    for _ in range(cant):
        x, error = Desapilar_registro(reservas, Reserva)
        
        fecha = x['entrada']
        
        entrada = datetime(int(fecha['anio']), int(fecha['mes']), int(fecha['dia']))
        
        diff = hoy - entrada
        
        if diff.days < 0:
            Apilar_registro(pila_aux, x)
            continue
        
        Apilar_registro(purgadas, x)
    
    Volver_a_apilar_registros(reservas, pila_aux, Reserva)
    return purgadas


def Buscar_siguiente_reserva(vec_hab, tipo, nhab, reservas):
    cant_reservas = len(reservas)
    
    pila_aux = []
    Crear_pila(pila_aux)
    b = 0
    
    Volver_a_apilar_registros(pila_aux, reservas, Reserva)
    
    for _ in range(cant_reservas):
        x, error = Desapilar_registro(pila_aux, Reserva)
        
        if error: break
        
        num = int(x['numHabitacion'])
        
        if num != nhab:
            Apilar_registro(reservas, x)
            continue 
        
        entrada = x['entrada']
        salida = x['salida']
        
        if not Verificar_disponibilidad(vec_hab, tipo, entrada, salida):
            Apilar_registro(reservas, x)
            continue
        
        Apilar_registro(reservas, x)
        b = 1
        
        break
    Volver_a_apilar_registros(reservas, pila_aux, Reserva)
    
    if b == 1:
        return x
    
    return None

def Confirmar_ocupacion(ocupaciones, nHab):
    cant_ocup = len(ocupaciones)
    
    pila_aux = []
    Crear_pila(pila_aux)
    b = 0
    
    for _ in range(cant_ocup):
        x, _ = Desapilar_registro(ocupaciones, Ocupacion)
        
        if int(x['numHabitacion']) == nHab:
            b = 1
        
        Apilar_registro(pila_aux, x)
    
    Volver_a_apilar_registros(ocupaciones, pila_aux, Ocupacion)
    
    if not b:
        return False
    
    return True


# Conversión

def Indice_a_mes(indice):
    meses = [
        'enero',
        'febrero',
        'marzo',
        'abril',
        'mayo',
        'junio',
        'julio',
        'agosto',
        'septiembre',
        'octubre',
        'noviembre',
        'diciembre'
        ] # Lista con los meses del año
    
    return meses[indice]


# Pedir datos

def Pedir_tipo(precios, tipos, especificacion):
    while True:
        print(f'###\t\tIngrese el tipo de {especificacion}\t\t###\n')
        Mostrar_precios(precios, tipos)
        print('# Escriba "Cancelar" para salir #')
        res = input('# ').upper()
        
        if res.lower() == 'cancelar':
            return False
        
        if not res in tipos:
            print('# Ingrese un tipo válido #')
            Limpiar_consola(1)
            continue 
        
        return res


def Pedir_precio():
    while True:
        print('###\t\tIngrese el precio a establecer\t\t###')
        print('# Escriba 0 para salir #')
        try:
            res = float(input('# '))
        except ValueError:
            print('# Ingrese un precio válido #')
            Limpiar_consola(1)
            continue 
        
        if res == 0:
            return False 
        
        return res


def Pedir_fecha(especificacion):
    fecha=np.empty(1,dtype=Fecha)
    
    while True:
        print(f'###\t\tIngrese la fecha de {especificacion}\t\t###')
        print('# Escriba 0 en algún parametro para cancelar #')
        try:
            dia = int(input("ingrese el dia: "))
            mes = int(input("ingrese el mes: "))
            anio = int(input("ingrese el año: "))
        except ValueError:
            print('# Ingrese una fecha válida #')
            Limpiar_consola(1)
            continue

        if dia * mes * anio == 0:
            return False

        if not Es_fecha_valida(anio, mes, dia):
            print('# Ingrese una fecha válida #')
            Limpiar_consola(1)
            continue

        fecha["dia"] = dia
        fecha["mes"] = mes
        fecha["anio"] = anio

        return fecha


def Pedir_numero_entero(tipo):
    while True:
        print(f'###\t\tIngrese el numero de {tipo}\t\t###\n# Escriba 0 para cancelar #\n')
        
        try:
            num = int(input("# "))
        except ValueError:
            print(f'# Ingrese un numero de {tipo} válido #')
            Limpiar_consola(1)
            continue
        
        if num == 0:
            return False
        
        return num


def Pedir_nombre(tipo, femenino = False):
    conector = 'de la' if femenino else 'del'
    while True:
        print(f'###\t\tIngrese el nombre {conector} {tipo}\t\t###\n')
        print('# Escriba "Cancelar" para salir #')
        res = input('# ')
        
        if res.lower() == 'cancelar':
            return False
        
        if len(res) < 1:
            print('# Ingrese un nombre válido #')
            Limpiar_consola(1)
            continue
        
        return res.capitalize()


def Pedir_fecha_nacimiento():
    fecha = Pedir_fecha('Nacimiento')
    
    if not fecha: return False, 'Cancelado'
    
    if not Es_mayor(fecha): return False, 'Menor'
    
    return fecha


def Pedir_domicilio():
    domicilio=np.empty(1,dtype=Domicilio)
    
    domicilio["calle"] = Pedir_nombre('calle', True)
    
    if not domicilio['calle']:
        return False
    
    domicilio["numero"] = Pedir_numero_entero('calle')
    
    if not domicilio['numero']:
        return False
    
    domicilio["ciudad"] = Pedir_nombre('ciudad', True)
    
    if not domicilio['ciudad']:
        return False
    
    domicilio["provincia"] = Pedir_nombre('provincia', True)
    
    if not domicilio['provincia']:
        return False
    
    return domicilio


def Pedir_tarjeta():
    nTarjeta = False 
    while not nTarjeta:
        nTarjeta = ''
        primeros = Pedir_numero_entero('los primeros 4 caracteres de la tarjeta')
        
        if not primeros:
            return False
        
        segundos = Pedir_numero_entero('los segundos 4 caracteres de la tarjeta')
        
        if not segundos:
            return False
        
        terceros = Pedir_numero_entero('los terceros 4 caracteres de la tarjeta')
        
        if not terceros:
            return False
        
        cuartos = Pedir_numero_entero('los cuartos 4 caracteres de la tarjeta')
        
        if not terceros:
            return False
        
        nTarjeta = str(primeros) + str(segundos) + str(terceros) + str(cuartos)

        if len(nTarjeta) != 16:
            print('# Ingrese un numero de tarjeta válido #')
            nTarjeta = False
            Limpiar_consola(1)
            continue
        
        return nTarjeta