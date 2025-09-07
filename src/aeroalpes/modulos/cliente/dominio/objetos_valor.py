"""Objetos valor del dominio de cliente

En este archivo usted encontrará los objetos valor del dominio de cliente

"""

from aeroalpes.seedwork.dominio.objetos_valor import ObjetoValor, Ciudad
from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class Nombre(ObjetoValor):
    nombres: str
    apellidos: str

@dataclass(frozen=True)
class Email(ObjetoValor):
    address: str
    dominio: str
    es_empresarial: bool

@dataclass(frozen=True)
class Cedula(ObjetoValor):
    numero: int
    ciudad: Ciudad

@dataclass(frozen=True)
class Rut(ObjetoValor):
    numero: int
    ciudad: Ciudad

# tipo: tarjeta de crédito, débito, transferencia bancaria
# nombre cambiable
# datos ofuscados: num tarjeta, cvv, fecha expiracion
# token persistente de seguridad: token unico

# "tarjeta_credito", "tarjeta_debito", "transferencia_bancaria"
class TipoPagoEnum(Enum):
    TARJETA_CREDITO = "tarjeta_credito"
    TARJETA_DEBITO = "tarjeta_debito"
    TRANSFERENCIA_BANCARIA = "transferencia_bancaria"

@dataclass(frozen=True)
class TipoPago(ObjetoValor):
    tipo: TipoPagoEnum  

# No existe un nombre metodo de pago porque sería hacer sobre ingenieria.
# No vale crear un Value Object por que no:
# - existe logica de validacion compleja
# - existe comportamiento especifico
# - composicion de multiples atributos
# - reutilizacion en multiples contextos
# 
# @dataclass(frozen=True) 
# class NombreMetodoPago(ObjetoValor):
#    nombre: str  # Nombre personalizable por el usuario

@dataclass(frozen=True)
class TokenSeguridad(ObjetoValor):
    token: str  # Token único persistente para recuperar datos

@dataclass(frozen=True)
class DatosOfuscados(ObjetoValor):
    ultimos_digitos: str  # Solo últimos 4 dígitos
    marca: str  # Visa, Mastercard, etc.
