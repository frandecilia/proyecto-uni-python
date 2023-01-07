# --<>----<>----<>----< Imports >----<>----<>----<>-- #

from Tool_functions import Es_fecha_valida, Indice_a_mes
from datetime import datetime

# --<>----<>----<>----< Funciones >----<>----<>----<>-- #

# Cargar precios

def Cargar_precios_servicios(precios):
    """
    Esta funcion carga los precios de los servicios del hotel
    
    :param precios: Registro que almacena los precios de los servicios del hotel
    :return: None
    """
    precios['FRIGOBAR'] = 299.99
    precios['ROOM-SERVICE'] = 489.99
    precios['LAVANDERIA'] = 179.99
    precios['BAR'] = 159.99
    precios['SPA'] = 369.99
    precios['GIMNASIO'] = 249.99
    
    return None


def Cargar_precios_habitaciones(precios, tipos):
    """
    Procedimiento encargado de cargar precios por defecto dentro del registro
    
    :param precios: Registro con los precios para cada tipo de habitación
    :param tipos: Vector con los tipos de habitacion
    :return: none
    """
    
    precio_default = 1499.99
    aumento = 2000
    
    for i in range(len(tipos)):
        tipo = tipos[i]
        precios[tipo] = precio_default
        precio_default += aumento
    
    return None


# Cargar valores por defecto

def Cargar_calendario(vec_hab, i, mes_inicial, mes_final, dia_inicial, dia_final, valor):
    anio_actual = datetime.now().year
    
    # Necesario por limitaciones con Numpy
    mes_inicial = int(mes_inicial)
    mes_final = int(mes_final)
    dia_inicial = int(dia_inicial)
    dia_final = int(dia_final)
    
    for indice_mes in range((mes_inicial - 1), 12):
        for dia in range((dia_inicial - 1), 31):
            
            if not Es_fecha_valida(anio_actual, indice_mes + 1, dia + 1):
                continue
            
            if indice_mes == mes_inicial - 1 and dia < dia_inicial - 1:
                continue
            
            if indice_mes == mes_final - 1 and dia > dia_final - 1:
                continue
            
            mes = Indice_a_mes(indice_mes)
            vec_hab[i]['diario'][mes][dia] = valor
    
    return None


def Cargar_tipo_habitaciones(vec_hab, cantidad, cont, i, tipo, precio):
    """
    Procedimiento encargado de llenar los registros indicados con información por defecto para su posterior uso
    
    :param vec_hab: Vector con los registros de las habitaciones
    :param cantidad: Cantidad específica de habitaciones a generar
    :param cont: Contador con el numero a asignar para las habitaciones
    :param i: Índice a asignar dentro del vector de registros
    :param tipo: Tipo a asignar en las habitaciones
    :param precio: Precio específico para el determinado tipo de habitación
    :return: El indice para las próximas asignaciones
    """
    for num in range(cantidad):
        vec_hab[i]['numero'] = cont
        vec_hab[i]['tipo'] = tipo
        vec_hab[i]['precio'] = precio
        
        Cargar_calendario(vec_hab, i, 1, 12, 1, 31, 'Disponible')
        
        vec_hab[i]['habilitada'] = True
        
        i+=1
        cont+=1

    return i


def Cargar_habitaciones(vec_hab, tipos, cantidades, precios):
    """
    Procedimiento encargado de llamar a la función de carga para cada tipo de habitación, llevando a cabo también
    el manejo del número de habitación correspondiente para cada tipo
    
    :param vec_hab: Vector de los registros de cada habitación
    :param tipos: Vector con cada tipo de habitación
    :param cantidades: Vector con cada cantidad correspondiente para cada tipo de habitación
    :param precios: Registro con los precios para cada tipo de habitación
    :return: None
    """
    
    i = 0
    for j in range(3):
        tipo = tipos[j]
        num_id = j * 100 + 200
        i = Cargar_tipo_habitaciones(vec_hab, cantidades[j], num_id, i, tipo, precios[tipo])
    
    return None


def Cargar_huespedes_num(vec, cant_hab, max_inv):
    """
    Procedimiento encargado de establecer un 0 en cada campo 'numero' de los huespedes, para una gestión más sencilla posteriormente

    :param vec: Vector con los registros de huespedes
    :param cant_hab: Cantidad total de habitaciones del hotel
    :param max_inv: Cantidad máxima de invitados por huesped
    :return: None
    """
    
    for i in range(cant_hab):
        for j in range(max_inv):
            vec[j, i]['numHabitacion'] = 0
    
    return None

