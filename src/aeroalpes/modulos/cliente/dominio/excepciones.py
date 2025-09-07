"""Excepciones del dominio de cliente

En este archivo usted encontrará las diferentes excepciones del dominio de cliente

"""

from aeroalpes.seedwork.dominio.excepciones import ExcepcionDominio

class ExcepcionDominioCliente(ExcepcionDominio):
    """Excepción base para el dominio de cliente"""
    ...

class TipoObjetoNoExisteEnDominioClienteExcepcion(ExcepcionDominioCliente):
    def __init__(self, mensaje='El objeto no hace parte del dominio de cliente'):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)

class EmailInvalidoExcepcion(ExcepcionDominioCliente):
    def __init__(self, mensaje='El email no tiene un formato válido'):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)

class UsuarioSinMetodoPagoExcepcion(ExcepcionDominioCliente):
    def __init__(self, mensaje='El usuario debe tener al menos un método de pago válido'):
        self.__mensaje = mensaje

    def __str__(self):
        return str(self.__mensaje)
