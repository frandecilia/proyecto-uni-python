# --<>----<>----<>----< Imports >----<>----<>----<>-- #

import numpy as np

# --<>----<>----<>----< Funciones >----<>----<>----<>-- #

def Crear_pila(pila):
    pila = []
    return  None


def Apilar(pila, elemento):
    error = False
    pila.append(elemento)
    return error


def Apilar_registro(pila, elemento):
    error = False
    pila.append(elemento.copy())
    return error


def Desapilar(pila):
    if not Pila_vacia(pila):
        ultimo = len(pila) - 1
        elemento = pila.pop(ultimo)
        error = False
    else:
        error = True
    return (elemento, error)


def Desapilar_registro(pila, tipo):
    elemento = np.empty(1, dtype= tipo)
    if not Pila_vacia(pila):
        ultimo = len(pila) - 1
        elemento = pila.pop(ultimo)
        error = False
    else:
        error = True
    return (elemento, error)


def Pila_vacia(pila):
    if len(pila)==0:
        vacia = True
    else:
        vacia = False
    return vacia


def Volver_a_apilar(pila, pilaAux):
    cant = len(pilaAux)
    
    for i in range(cant):
        x, _ = Desapilar(pilaAux)
        
        Apilar(pila, x)
    
    return None


def Volver_a_apilar_registros(pila, pilaAux, tipo):
    cant = len(pilaAux)
    
    for _ in range(cant):
        x, _ = Desapilar_registro(pilaAux, tipo)
        
        Apilar_registro(pila, x)
    
    return None
