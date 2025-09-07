"""Excepciones para la capa de infraestructura del dominio de cliente

En este archivo usted encontrará las diferentes excepciones de la capa de infraestructura

"""

from aeroalpes.seedwork.dominio.excepciones import ExcepcionDominio

class ExcepcionInfraestructuraCliente(ExcepcionDominio):
    """Excepción base para la infraestructura de cliente"""
    ...

class ExcepcionFabrica(ExcepcionInfraestructuraCliente):
    def __init__(self, mensaje='Error en la fábrica de repositorios'):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)

class ExcepcionRepositorio(ExcepcionInfraestructuraCliente):
    def __init__(self, mensaje='Error en el repositorio'):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)
