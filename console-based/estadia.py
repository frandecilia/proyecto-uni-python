import numpy as np

def dias_de_estadia(fd,fh):
    anio_hasta=fh[0]['anio']
    mes_hasta = fh[0]['mes']
    dia_hasta = fh[0]['dia']
    anio_desde = fd[0]['anio']
    mes_desde = fd[0]['mes']
    dia_desde = fd[0]['dia']
    anio = anio_desde
    dias = 0
    while anio <= anio_hasta:
        mes_inicio = 1
        mes_fin = 12
        if anio == anio_desde:
            mes_inicio = mes_desde
        if anio == anio_hasta:
            mes_fin = mes_hasta
        while mes_inicio <= mes_fin:
            if (mes_inicio == mes_hasta) and (anio == anio_hasta):
                dias = dias + dia_hasta
            elif (mes_inicio == 4) or (mes_inicio == 6) or (mes_inicio == 9) or (mes_inicio == 11):
                dias = dias + 30
            elif mes_inicio == 2:
                if es_anio_bisiesto(anio):
                    dias = dias + 29
                else:
                    dias = dias + 28
            else:
                dias = dias + 31
            if (mes_inicio == mes_desde) and (anio == anio_desde):
                dias = dias - dia_desde
            mes_inicio = mes_inicio + 1
        anio = anio + 1
    return dias


def es_anio_bisiesto(anio):
    if (anio % 4==0 and anio % 100!=0) or (anio % 400==0):
        es_bisiesto = True
    else:
        es_bisiesto = False
    return es_bisiesto

