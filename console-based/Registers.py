# --<>----<>----<>----< Imports >----<>----<>----<>-- #

import numpy as np

# --<>----<>----<>----< Registros >----<>----<>----<>-- #

Calendario = np.dtype([
    ('enero', 'U10', 31),
    ('febrero', 'U10', 29),
    ('marzo', 'U10', 31),
    ('abril', 'U10', 30),
    ('mayo', 'U10', 31),
    ('junio', 'U10', 30),
    ('julio', 'U10', 31),
    ('agosto', 'U10', 31),
    ('septiembre', 'U10', 30),
    ('octubre', 'U10', 31),
    ('noviembre', 'U10', 30),
    ('diciembre', 'U10', 31)
])

Habitacion = np.dtype([
    ('numero', int),
    ('tipo', 'U1'),
    ('precio', float),
    ('diario', Calendario),
    ('habilitada', bool)
])

Domicilio = np.dtype([
    ('calle', 'U64'),
    ('numero', int),
    ('ciudad', 'U64'),
    ('provincia', 'U64')
])

PrecioHabitaciones = np.dtype([
    ('D', float),
    ('T', float),
    ('C', float)
])

Fecha = np.dtype([
    ('dia', 'int'),
    ('mes', 'int'),
    ('anio', 'int')
])

Huesped = np.dtype([
    ('dni', int),
    ('nombreCompleto', 'U70'),
    ('domicilio', Domicilio),
    ('fechaNacimiento', Fecha),
    ('esResponsable', bool),
    ('dniACargo', int),
    ('numHabitacion', int),
    ('numTarjeta', 'U16')
])

Reserva = np.dtype([
    ('numHabitacion', int),
    ('entrada', Fecha),
    ('salida', Fecha),
    ('dniACargo', int)
])

Ocupacion = np.dtype([
    ('numHabitacion', int),
    ('checkIn', Fecha),
    ('checkOut', Fecha),
    ('dniACargo', int)
])

PrecioServicios = np.dtype([
    ('FRIGOBAR', float),
    ('ROOM-SERVICE', float),
    ('LAVANDERIA', float),
    ('BAR', float),
    ('SPA', float),
    ('GIMNASIO', float)
])

Servicio = np.dtype([
    ('nombre', 'U12'),
    ('numHabitacion', int),
    ('codigo', int),
    ('cantidad', int)
])

