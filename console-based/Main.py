# --<>----<>----<>----< Imports >----<>----<>----<>-- #

import numpy as np
from Tool_functions import *
from Setup_functions import *
from Registers import *
from Management_functions import *

# --<>----<>----<>----< Funciones >----<>----<>----<>-- #


def Debugeo_ver_registro(vec, tipo = 'Habitaciones'):
    largo_vec = len(vec)
    if tipo == 'Huespedes':
        largo_vec = Determinar_indice_huespedes(vec)
    for i in range(largo_vec):
        print('#'*80)
        print(f'# {i + 1} #')
        print(vec[i])
        print('#' * 80)


# --<>----<>----<>----< Inicialización de variables >----<>----<>----<>-- #

TIPOS_HAB = np.array(['D', 'T', 'C'], dtype='U1') # Vector con los tipos de habitación disponibles
TIPOS_SERV = np.array([
    'FRIGOBAR',
    'ROOM-SERVICE',
    'LAVANDERIA',
    'BAR',
    'SPA',
    'GIMNASIO'
    ], dtype='U12') # Vector con los tipos de servicios disponibles
CANT_HAB = np.array([
                        10, # Cantidad de habitaciones dobles 
                        8, # Cantidad de habitaciones triples
                        7 # Cantidad de habitaciones cuadruples
                    ], dtype=int)
MAX_ACOMP = 8
TOTAL_HAB = Cantidad_habitaciones(CANT_HAB)

precios_habitaciones = np.empty(1, dtype = PrecioHabitaciones)
precios_servicios = np.empty(1, dtype= PrecioServicios)
lista_habitaciones = np.empty(TOTAL_HAB, dtype = Habitacion)
lista_clientes = np.empty([MAX_ACOMP+1, TOTAL_HAB*100], dtype = Huesped)

reservas = [] # Cola de reservas
Crear_pila(reservas)

servicios = []
Crear_pila(servicios)

ocupaciones = []
Crear_pila(ocupaciones)

# --<>----<>----<>----< Setup >----<>----<>----<>-- #

Cargar_precios_habitaciones(precios_habitaciones, TIPOS_HAB)
Cargar_precios_servicios(precios_servicios)
Cargar_habitaciones(lista_habitaciones, TIPOS_HAB, CANT_HAB, precios_habitaciones)
Cargar_huespedes_num(lista_clientes, TOTAL_HAB, MAX_ACOMP)

# --<>----<>----<>----< Main app >----<>----<>----<>-- #

while True:
    
    Limpiar_consola(1)
    
    Mostrar_logo()
    res = Menu_opciones(
        'Reserva de habitación',
        'Ingreso de Pasajeros – Check In',
        'Servicios por Habitación',
        'Egreso de Pasajeros – Check Out',
        'Cancelación de Reservas',
        'Informes',
        'Tareas Diarias',
        'Modificar Precios',
        'Salir',
        '[DEBUG] Mostrar vector/registro/pila'
    )
    
    Limpiar_consola(1)
    
    if res == 9:
        break
    
    if res == 1:
        dniReserva, indice = Toma_de_datos(lista_clientes)
        
        if not dniReserva and not indice:
            print('# Se canceló la toma de datos del huesped #')
            Limpiar_consola(1)
            continue
        
        h = Proceso_de_reserva(lista_clientes, MAX_ACOMP, lista_habitaciones, TIPOS_HAB, precios_habitaciones, reservas, dniReserva, indice)
        
        if not h:
            print('# Se canceló la búsqueda de habitaciones #')
            Actualizar_huespedes(lista_clientes)
            Limpiar_consola(1)
            continue
        
        print('# Se ha reservado con éxito #')
    
    if res == 2:
        res = Menu_opciones(
                            'Hacer Check-In a partir de una reserva',
                            'Buscar habitaciones disponibles en el instante',
                            'Salir'
                            )
        
        if res == 3: continue
        
        Limpiar_consola(1)
        
        if res == 1:
            dni = Pedir_numero_entero('DNI de la reserva a buscar')
            
            if not dni:
                print('# Se canceló la busqueda de la reserva #')
                Limpiar_consola(1)
                continue
            
            Limpiar_consola(1)
            
            Proceso_check_in(ocupaciones, reservas, dni, lista_habitaciones)

        if res == 2:
            dniReserva, indice = Toma_de_datos(lista_clientes)
            
            if not dniReserva and not indice:
                continue
            
            habitaciones = Proceso_de_reserva(lista_clientes, MAX_ACOMP, lista_habitaciones, TIPOS_HAB, precios_habitaciones, reservas, dniReserva, indice)
            
            if not habitaciones:
                continue
            
            cant = len(habitaciones)
            for i in range(cant):
                x, error = Desapilar(habitaciones)
                
                if error: break
                
                Proceso_check_in(ocupaciones, reservas, dniReserva, lista_habitaciones)
    
    if res == 3:
        res = Menu_opciones(
                            'Agregar pago de servicios a una habitación',
                            'Salir'
                            )
        if res == 2: continue 
        
        nHab = Pedir_numero_entero('habitación a cargar')
        
        if not nHab:
            print('# Se canceló la busqueda de habitación #')
            Limpiar_consola(1)
            continue
        
        index = Buscar_hab_por_num(lista_habitaciones, nHab)
        
        if type(index) != int:
            print(f'# La habitación de número {nHab} no existe #')
            Limpiar_consola(1)
            continue
        
        if not Confirmar_ocupacion(ocupaciones, nHab):
            print(f'# La habitación de número {nHab} no está ocupada #')
            Limpiar_consola(1)
            continue
        
        error = Proceso_carga_de_servicios(nHab, precios_servicios, TIPOS_SERV, servicios)
        
        if error:
            print('# Se canceló la carga de servicios a la habitacion #')
            Limpiar_consola(1)
            continue
        
        print(f'# Servicios cargados a la habitación {nHab} con exito #')
    
    if res == 4:
        dni = Pedir_numero_entero('DNI de la ocupación a concretar')
        
        if not dni:
            print('# Se canceló la busqueda de ocupación #')
            Limpiar_consola(1)
            continue
        
        Limpiar_consola(1)
        
        Proceso_check_out(ocupaciones, dni, lista_habitaciones, lista_clientes, servicios, precios_servicios)
    
    if res == 5:
        dni = Pedir_numero_entero('DNI de la reserva a cancelar')
        
        if not dni:
            print('# Se canceló la busqueda de la reserva #')
            Limpiar_consola(1)
            continue
        
        Limpiar_consola(1)
        
        Proceso_cancelar_reserva(reservas, dni, lista_habitaciones)
        print('# Reserva cancelada con éxito #')
    
    if res == 6:
        res = Menu_opciones(
                            'Generar informe de huespedes para hoy',
                            'Generar informe de menores',
                            'Cancelar'
                            )
        
        if res == 3:
            continue
        if res == 1:
            Informe_huespedes(lista_clientes, reservas)
        if res == 2:
            Informe_menores(lista_clientes, ocupaciones)
    
    if res == 7:
        res = Menu_opciones(
                            'Extender estadia I Modificar fecha de salida',
                            'Purgar reservas',
                            'Cancelar'
                            )
        
        if res == 3:
            continue
        
        Limpiar_consola(1)
        
        if res == 1:
            Extender_estadia(ocupaciones)
        if res == 2:
            Purgar_reservas_expiradas(reservas, lista_habitaciones, lista_clientes)
    
    if res == 8:
        res = Menu_opciones(
            'Modificar precios de los servicios',
            'Modificar precios de las habitaciones',
            'Salir'
        )
        
        if res == 3:
            continue 
        
        if res == 1:
            Modificar_precios_servicios(precios_servicios, TIPOS_SERV)
            continue
        
        if res == 2:
            Modificar_precios_habitaciones(precios_habitaciones, TIPOS_HAB)
            Actualizar_precios_hab(lista_habitaciones, precios_habitaciones)
            continue
    
    if res == 10:
        res = Menu_opciones(
                            'Servicios',
                            'Habitaciones',
                            'Huespedes',
                            'Ocupaciones',
                            'Reservas',
                            'Salir'
                            )
        
        if res == 6:
            continue
        
        if res == 1:
            print(servicios)
        if res == 2:
            Debugeo_ver_registro(lista_habitaciones)
        if res == 3:
            Debugeo_ver_registro(lista_clientes, 'Huespedes')
        if res == 4:
            print(ocupaciones)
        if res == 5:
            print(reservas)
        input('Presione enter para continuar')
