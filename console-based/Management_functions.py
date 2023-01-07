# --<>----<>----<>----< Imports >----<>----<>----<>-- #

from Registers import *
from random import randint
from Setup_functions import Cargar_calendario
from Tool_functions import *
from Pila_functions import *
from estadia import dias_de_estadia

# --<>----<>----<>----< Funciones >----<>----<>----<>-- #

def Modificar_precios_habitaciones(precios, tipos):
    """
    Procedimiento encargado de modificar el precio para el tipo de habitación especificado

    :param precios: Registro que almacena los precios de los servicios del hotel
    :param tipos: Vector que almacena los tipos de servicios disponibles
    :return: None
    """
    tipo = Pedir_tipo(precios, tipos, 'habitación')
    
    if not tipo:
        return False
    Limpiar_consola(1)
    
    precio = Pedir_precio()
    
    if not precio:
        return False
    Limpiar_consola(1)
    
    precios[tipo] = precio
    
    return None


def Modificar_precios_servicios(precios, tipos):
    """
    Procedimiento encargado de modificar el precio para el tipo de servicio especificado
    
    :param precios: Registro que almacena los precios de los servicios del hotel
    :param tipos: Vector que almacena los tipos de servicios disponibles
    :return: None
    """
    servicio = Pedir_tipo(precios, tipos, 'servicio')
    
    if not servicio:
        return None
    Limpiar_consola(1)
    
    precio = Pedir_precio()
    
    if not precio:
        return
    Limpiar_consola(1)
    
    precios[servicio] = precio
    
    return None


def Actualizar_precios_hab(vec, precios):
    CANT_HAB = len(vec)
    
    for i in range(CANT_HAB):
        tipo = vec[i]['tipo']
        vec[i]['precio'] = precios[tipo]
    
    return None


def Actualizar_huespedes(vec_huespedes):
    cant_i = len(vec_huespedes)
    cant_j = len(vec_huespedes[0])
    
    for j in range(cant_j):
        for i in range(cant_i):
            if int(vec_huespedes[i, j]['numHabitacion']) != 0:
                continue
            
            vec_huespedes[i, j]['dni'] = 0
            vec_huespedes[i, j]['nombreCompleto'] = ''
            vec_huespedes[i, j]['esResponsable'] = False
            vec_huespedes[i, j]['dniACargo'] = 0
            vec_huespedes[i, j]['numHabitacion'] = 0
            vec_huespedes[i, j]['numTarjeta'] = ''


def Guardar_huespedes(vec_huespedes, indice, dni, nombre, domicilio, fechaNac, esResponsable, dniACargo, numHab, numTarjeta):
    i, j = indice[0], indice[1]
    
    vec_huespedes[i, j]['dni'] = dni
    vec_huespedes[i, j]['nombreCompleto'] = nombre
    vec_huespedes[i, j]['domicilio'] = domicilio
    vec_huespedes[i, j]['esResponsable'] = esResponsable
    vec_huespedes[i, j]['fechaNacimiento'] = fechaNac
    vec_huespedes[i, j]['dniACargo'] = dniACargo
    vec_huespedes[i, j]['numHabitacion'] = numHab
    vec_huespedes[i, j]['numTarjeta'] = numTarjeta

    return True


def Guardar_reservas(vec_hab, reservas, habitaciones, dniACargo, entrada, salida):
    cant = len(habitaciones)
    reserva = np.empty(1, dtype = Reserva)
    aux = []
    Crear_pila(aux)
    
    for i in range(cant):
        x, error = Desapilar(habitaciones)
        
        if error: break 
        
        reserva['numHabitacion'] = x
        reserva['entrada'] = entrada
        reserva['salida'] = salida
        reserva['dniACargo'] = dniACargo
        
        Apilar_registro(reservas, reserva)
        Apilar(aux, x)

    Volver_a_apilar(habitaciones, aux)
    Cargar_calendario(vec_hab, i, int(entrada['mes']), int(salida['mes']), int(entrada['dia']), int(salida['dia']), 'Reservado')
    return None


def Guardar_check_in(ocupaciones, nHab, entrada, salida, dniACargo):
    check_in = np.empty(1, dtype=Ocupacion)
    
    check_in['numHabitacion'] = nHab
    check_in['checkIn'] = entrada
    check_in['checkOut'] = salida
    check_in['dniACargo'] = dniACargo
    
    Apilar(ocupaciones, check_in)


def Buscar_habitacion(tipo, entrada, salida, vec_hab, tipos, reservas):
    num_hab = False
    tipoHab = tipo
    
    while not num_hab:
        num_hab = Verificar_disponibilidad(vec_hab, tipoHab, entrada, salida)
        
        if num_hab: continue
        
        print(f'# No se encontró habitación de tipo {tipo} disponible para las fechas ingresadas #')
        Limpiar_consola(1)
        
        print('# ¿Como desea proseguir? #')
        res = Menu_opciones(
                            'Reservar en caso de que se libere',
                            'Buscar una habitación de tipo superior',
                            'Cancelar'
                            )
        
        if res == 3: return False
        
        if res == 2:
            tipoHab = Determinar_siguiente_tipo(tipos, tipo)
            
            if not tipoHab:
                print('# No existe tipo superior al ingresado #')
                tipoHab = tipo
                
                Limpiar_consola(1)
                continue
            
            continue
        
        if res == 1:
            num_hab = Buscar_menos_reservada(vec_hab, reservas, tipoHab) 
    
    return num_hab


def Preguntar_hospedaje(vec_hab, tipos, precios, dniReserva, reservas):
    habitaciones = []
    Crear_pila(habitaciones)
    
    Limpiar_consola(1)
    
    entrada = Pedir_fecha('entrada')
    
    if not entrada:
        print('# Se canceló el ingreso de fecha de entrada #')
        Limpiar_consola(1)
        return None
    
    Limpiar_consola(1)
    
    salida = Pedir_fecha('salida')
    
    if not entrada:
        print('# Se canceló el ingreso de fecha de salida #')
        Limpiar_consola(1)
        return None

    Limpiar_consola(1)

    while True:
        if len(habitaciones) > 0:
            res = Menu_opciones(
                            'Reservar otra habitación',
                            'Reservas finalizadas'
                            )
            
            if res == 2: break
        
        tipo = Pedir_tipo(precios, tipos, 'la habitación a reservar')
        
        if not tipo:
            print('# Se canceló la selección de habitaciones #')
            Limpiar_consola(1)
            
            if len(habitaciones) < 1:
                return None
            
            continue
        
        num_hab = Buscar_habitacion(tipo, entrada, salida, vec_hab, tipos, reservas)
        
        if not num_hab:
            print('# Se canceló la reserva de habitaciones #')
            Limpiar_consola(1)
            
            if len(habitaciones) < 1:
                return None
            
            continue
        
        Apilar(habitaciones, num_hab)
    
    Guardar_reservas(vec_hab, reservas, habitaciones, dniReserva, entrada, salida)
    return habitaciones


def Datos_huesped(vec_huespedes, indice, aCargo = True, numHab = 0):
    dni = Pedir_numero_entero('DNI')
    
    if not dni:
        print("# Se canceló el ingreso de DNI #")
        Limpiar_consola(1)
        return None
    
    Limpiar_consola(1)
    
    nombre = Pedir_nombre('huesped completo')
    
    if not nombre:
        print("# Se canceló el ingreso del nombre #")
        Limpiar_consola(1)
        return None
    
    Limpiar_consola(1)
    
    domicilio = Pedir_domicilio()
    
    if not domicilio:
        print("# Se canceló el ingreso de domicilio #")
        Limpiar_consola(1)
        return None
    
    Limpiar_consola(1)
    
    if aCargo:
        fecha = Pedir_fecha_nacimiento()
        
        if not fecha[0]:
            mensaje = "# El huesped debe ser mayor de edad para reservar una habitación #" if fecha[1] == 'Menor' else '# Ingreso de fecha cancelado #'
            print(mensaje)
            Limpiar_consola(1)
            return None
        
        Limpiar_consola(1)
        
        numTarjeta = Pedir_tarjeta()
        
        if type(numTarjeta) != str:
            print("# Se canceló el ingreso de tarjeta #")
            Limpiar_consola(1)
            return None
    else:
        fecha = Pedir_fecha('nacimiento del huesped')
        
        if not fecha:
            print("# Se canceló el ingreso de fecha #")
            Limpiar_consola(1)
            return None

        numTarjeta = ''
    
    
    if not Es_mayor(fecha):
        Limpiar_consola(1)
        
        dniACargo = Pedir_numero_entero('DNI del huesped a cargo del menor')
        
        if not dniACargo:
            print("# Se canceló el ingreso de DNI #")
            Limpiar_consola(1)
            return None
        
        esResponsable = False
    else:
        dniACargo = 0
        esResponsable = True
    
    Guardar_huespedes(vec_huespedes, indice, dni, nombre, domicilio, fecha, esResponsable, dniACargo, numHab, numTarjeta)
    return dni


def Toma_de_datos(vec_huespedes):
    indice = Determinar_indice_huespedes(vec_huespedes)
    
    if indice is None:
        print('# Error inesperado, no se encuentran posiciones libres en el vector de huespedes #')
        return False, False
    
    dniReserva = Datos_huesped(vec_huespedes, (0, indice))
    
    if not dniReserva:
        print('# Se canceló el ingreso del huesped #')
        Limpiar_consola(1)
        return False, False
    return dniReserva, indice


def Proceso_de_reserva(vec_huespedes, max_acomp, vec_hab, tipos, precios, reservas, dniReserva, indice):
    habitaciones = Preguntar_hospedaje(vec_hab, tipos, precios, dniReserva, reservas)
    
    if not habitaciones:
        print('# Se canceló el ingreso de las habitaciones #')
        Limpiar_consola(1)
        return False
    
    i, j = Buscar_huesped_por_dni(vec_huespedes, dniReserva)
    
    vec_huespedes[i, j]['numHabitacion'] = habitaciones[0]
    pila_aux = []
    Crear_pila(pila_aux)
    
    for i in range(len(habitaciones)):
        cont = 0
        x, error = Desapilar(habitaciones)
        
        if error:
            break
        
        Apilar(pila_aux, x)
        
        while cont < max_acomp:
            if indice is None:
                print('# Error inesperado, no se encuentran posiciones libres en el vector de huespedes #')
                break
            
            res = Menu_opciones(
                                f'Agregar otro huesped acompañante a la habitación {x}',
                                'Finalizar ingreso de acompañantes para esta habitación'
                                )
            
            if res == 2:
                break
            
            Datos_huesped(vec_huespedes, (i + 1, indice), aCargo = False, numHab = x)
        indice = Determinar_indice_huespedes(vec_huespedes)
    
    Volver_a_apilar(habitaciones, pila_aux)
    return habitaciones


def Proceso_check_in(ocupaciones, reservas, dni, vec_hab):
    reserva = Buscar_por_dni(reservas, dni, Reserva)
    
    if not reserva:
        print('# No se encontró una reserva a nombre de este dni #')
        Limpiar_consola(1)
        return False
    
    Limpiar_consola(1)
    
    nHab = int(reserva['numHabitacion'])
    
    index = Buscar_hab_por_num(vec_hab, nHab)
    
    entrada = reserva['entrada']
    salida = reserva['salida']
    
    Limpiar_consola(1)
    
    Cargar_calendario(vec_hab, index, entrada['mes'], salida['mes'], entrada['dia'], salida['dia'], 'Ocupado')
    Guardar_check_in(ocupaciones, nHab, entrada, salida, dni)
    print('# Check-In exitoso #')


def Proceso_carga_de_servicios(nHab, precios, servicios, serviciosHab):
    tipo_servicio = Pedir_tipo(precios, servicios, 'servicio a cargar')
    
    if not tipo_servicio:
        print('# Se canceló la selección de tipo de servicio #')
        Limpiar_consola(1)
        return True
    
    cantidad = Pedir_numero_entero('veces que desea cargarle el servicio')
    
    if not cantidad:
        print('# Se canceló el ingreso de cantidad #')
        Limpiar_consola(1)
        return True
    
    servicio = np.empty(1, dtype= Servicio)
    servicio['nombre'] = tipo_servicio.upper()
    servicio['numHabitacion'] = nHab
    servicio['codigo'] = randint(10, 99)
    servicio['cantidad'] = cantidad
    
    Apilar_registro(serviciosHab, servicio)
    return False


def Proceso_check_out(ocupaciones, dni, vec_hab, vec_huespedes, servicios, precios_serv):
    ocupacion = Buscar_por_dni(ocupaciones, dni, Ocupacion)
    
    if not ocupacion:
        print('# No se encontró una ocupacion a nombre de este dni #')
        Limpiar_consola(1)
        return False
    
    Limpiar_consola(1)
    
    nHab = int(ocupacion['numHabitacion'])
    
    i, j = Buscar_huesped_por_dni(vec_huespedes, dni)
    index = Buscar_hab_por_num(vec_hab, nHab)
    
    huesped = vec_huespedes[i, j]
    habitacion = vec_hab[index]
    
    entrada = ocupacion['checkIn']
    salida = ocupacion['checkOut']
    
    Limpiar_consola(1)
    
    servicios_hab = Obtener_servicios_por_hab(nHab, servicios)
    
    Cargar_calendario(vec_hab, index, entrada['mes'], salida['mes'], entrada['dia'], salida['dia'], 'Disponible')
    Ticket_salida(huesped, dni, habitacion, precios_serv, entrada, salida, servicios_hab)
    input('\nPresione enter para continuar')
    
    Limpiar_consola(1)
    
    print('# Check-out exitoso #')


def Borrar_reserva(reserva, vec_hab, reservas):
    nHab = int(reserva['numHabitacion'])
    
    index = Buscar_hab_por_num(vec_hab, nHab)
    
    entrada = reserva['entrada']
    salida = reserva['salida']
    
    tipo = vec_hab[index]['tipo'][0]
    
    Cargar_calendario(vec_hab, index, entrada['mes'], salida['mes'], entrada['dia'], salida['dia'], 'Disponible')
    
    # Actualizando a la siguiente reserva
    
    sig_reserva = Buscar_siguiente_reserva(vec_hab, tipo, nHab, reservas)
    
    if not sig_reserva:
        return None
    
    nHab = int(sig_reserva['numHabitacion'])
    
    index = Buscar_hab_por_num(vec_hab, nHab)
    
    entrada = sig_reserva['entrada']
    salida = sig_reserva['salida']
    
    tipo = vec_hab[index]['tipo'][0]
    
    Cargar_calendario(vec_hab, index, int(entrada['mes']), int(salida['mes']), int(entrada['dia']), int(salida['dia']), 'Reservado')


def Proceso_cancelar_reserva(reservas, dni, vec_hab):
    reserva = Buscar_por_dni(reservas, dni, Reserva)
    
    if not reserva:
        print('# No se encontró una reserva a nombre de este dni #')
        Limpiar_consola(1)
        return False
    
    Limpiar_consola(1)
    
    Borrar_reserva(reserva, vec_hab, reservas)


def Ticket_salida(huesped, dni, habitacion, preciosServ, entrada, salida, servicios):
    domicilio = huesped["domicilio"]
    precio = float(habitacion['precio'])
    tipo_caracter = str(habitacion['tipo'])
    tipo = 'Doble' if tipo_caracter == 'D' else 'Triple' if tipo_caracter == 'T' else 'Cuadruple'
    dias = dias_de_estadia(entrada, salida)
    total_hab = precio * dias
    
    total = total_hab
    
    hoy = datetime.now()
    
    print('Hotel California\t\t\t\tFactura B')
    print(f'CUIT: 20-{dni}-{str(dni)[0]}')
    print('I.V.A RESPONSABLE INSCRIPTO')
    print(f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tFecha: {hoy.day}/{hoy.month}/{hoy.year}')
    print(f'Señor: {huesped["nombreCompleto"]}\t\t\tDNI: {dni}')
    print(f'Domicilio: {domicilio["calle"]} {domicilio["numero"]} - {domicilio["ciudad"]}, {domicilio["provincia"]}')
    print('|\tCantidad\t|\t\t\tDescripcion\t\t\t|\t\tPrecio Unitario\t\t|\t\tImporte\t\t|')
    print(f'|\t{dias}\t\t|\t\tNoches en Habitacion {tipo}\t\t|\t\t${precio}\t\t|\t\t${total_hab}\t|')
    
    while len(servicios) > 0:
        serv = np.empty(1, dtype= Servicio)
        serv, _ = Desapilar_registro(servicios, Servicio)
        cant_serv = int(serv["cantidad"])
        nombre_serv = str(serv["nombre"][0])
        
        if len(nombre_serv) < 4:
            nombre_serv+= ' '
        
        precio_serv =  float(preciosServ[nombre_serv])
        
        total_serv = precio_serv * cant_serv
        total += total_serv
        print(f'|\t{cant_serv}\t\t|\t\t\t{nombre_serv.capitalize()}\t\t\t|\t\t${precio_serv}\t\t|\t\t${total_serv}\t|')
    
    print(f'|\t\t\t|\t\t\t\t\t\t\t|\t\t\tTotal:\t\t|\t\t${total}\t|')


def Informe_huespedes(vec_huespedes, reservas):
    reservas_hoy = Obtener_reservas_para_hoy(reservas)
    
    if not reservas_hoy:
        print('# No hay huespedes con reservas para este día #')
        Limpiar_consola(2)
        return None
    
    cantidad_reservas = len(reservas_hoy)

    print('\t\t\t# Informe de huespedes para hoy #')
    print('|\tNumero de habitacion\t|\tNombre completo del huesped\t|\tDni')
    
    for i in range(cantidad_reservas):
        reserva = Obtener_reserva_hab_menor(reservas_hoy)
        
        nhab = int(reserva['numHabitacion'])
        dni = int(reserva['dniACargo'])
        i, j = Buscar_huesped_por_dni(vec_huespedes, dni)
        
        huesped = vec_huespedes[i, j]
        nombre = huesped['nombreCompleto']
        
        print(f'|\t\t\t{nhab}\t\t|\t{nombre}\t\t|\t{dni}|')
    
    input('# Presione enter para continuar #')


def Informe_menores(vec_huespedes, ocupaciones):
    
    cantidad_ocup = len(ocupaciones)
    
    pila_aux = []
    Crear_pila(pila_aux)
    
    b = 0
    
    for _ in range(cantidad_ocup):
        x, error = Desapilar_registro(ocupaciones, Ocupacion)
        
        if error: break
        
        nHab = int(x['numHabitacion'])
        
        Apilar_registro(pila_aux, x)
        
        hoy = datetime.now()
        huespedes = Obtener_huespedes_por_hab(vec_huespedes, nHab)
        
        if len(huespedes) < 2:
            continue
        
        menores, responsable = Obtener_menores_y_responsable(huespedes, int(x['dniACargo']))
        
        if len(menores) < 1:
            continue
        
        b = 1
        
        print(f'\t\t\tInforme de menores de edad del dia {hoy.day}/{hoy.month}/{hoy.year}')
        print(f'Habitacion: {nHab}\tNombre del responsable: {responsable["nombreCompleto"]}')
        print(f'Documento: {int(responsable["dni"])}')
        print('|\tDocumento\t|\t\t\tNombre completo\t\t\t|\t\tFecha de nacimiento\t\t|')
        
        while len(menores) > 0:
            x, error = Desapilar_registro(menores, Huesped)
            doc = int(x['dni'])
            nombre = str(x['nombreCompleto'])
            fechaNac = x['fechaNacimiento']
            
            print(f'|\t{doc}\t|\t\t\t{nombre}\t\t\t|\t\t\t{int(fechaNac["dia"])}/{int(fechaNac["mes"])}/{int(fechaNac["anio"])}\t\t|')
    Volver_a_apilar_registros(ocupaciones, pila_aux, Ocupacion)
    
    if b == 1:
        input('Presione enter para continuar')
        return None
    
    print('# No hay menores hospedándose actualmente #')


def Extender_estadia(ocupaciones):
    dni = Pedir_numero_entero('DNI de la ocupación')
    
    if not dni:
        print('# Se canceló la extensión de estadía #')
        Limpiar_consola(1)
        return None
    
    Limpiar_consola(1)
    
    ocupacion = Buscar_por_dni(ocupaciones, dni, Ocupacion)
    
    if not ocupacion:
        print('# No se encontró ocupación actual a ese DNI #')
        Limpiar_consola(1)
        return None
    
    Limpiar_consola(1)
    
    salida = Pedir_fecha('de salida a reestablecer')
    
    if not salida:
        print('# Se canceló la extension de estadía #')
        Limpiar_consola(1)
        return None
    
    Limpiar_consola(1)
    
    ocupacion['checkOut'] = salida
    
    Apilar_registro(ocupaciones, ocupacion)
    
    print('# Fecha de salida reestablecida #')


def Purgar_reservas_expiradas(reservas, vec_hab, vec_huespedes):
    purgadas = Obtener_reservas_vencidas(reservas)
    
    cant_purgadas = len(purgadas)
    
    if cant_purgadas < 1:
        print('# No se encontraron reservas vencidas #')
        Limpiar_consola(1)
        return None
    
    print('|\tDNI del huesped\t\t|\t\t\tNombre del huesped\t\t\t|\t\tTipo de habitacion\t\t|\t\tImporte\t\t|')
    
    for _ in range(cant_purgadas):
        x, error = Desapilar_registro(purgadas, Reserva)
        
        nHab = int(x['numHabitacion'])
        dni = int(x['dniACargo'])
        indexHab = Buscar_hab_por_num(vec_hab, nHab)
        indexHuesped = Buscar_huesped_por_dni(vec_huespedes, dni)
        
        huesped = vec_huespedes[indexHuesped[0], indexHuesped[1]]
        nombre = huesped['nombreCompleto'][0]
        
        habitacion = vec_hab[indexHab]
        tipo_caracter = habitacion['tipo'][0]
        tipo = 'Doble' if tipo_caracter == 'D' else 'Triple' if tipo_caracter == 'T' else 'Cuadruple'
        
        print(f'|\t\t{dni}\t\t|\t\t\t{nombre}\t\t\t|\t\tHabitacion {tipo}\t\t|\t\t${float(habitacion["precio"])}\t|')
        
        Borrar_reserva(x, vec_hab, reservas)
    
    input('Presione enter para continuar')