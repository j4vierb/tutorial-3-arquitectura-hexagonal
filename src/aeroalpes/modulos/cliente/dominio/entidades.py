"""Entidades del dominio de cliente

En este archivo usted encontrará las entidades del dominio de cliente

"""

from datetime import datetime
from aeroalpes.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass, field

from .objetos_valor import Nombre, Email, Cedula, Rut
from .objetos_valor import TipoPago, \
    TokenSeguridad, DatosOfuscados
from aeroalpes.seedwork.dominio.entidades import AgregacionRaiz

@dataclass
class MetodoPago(Entidad):  # Hereda de Entidad del seedwork
    tipo: TipoPago
    nombre: str  # Mutable
    token_seguridad: TokenSeguridad
    datos_ofuscados: DatosOfuscados
    activo: bool = True  # Mutable

    def cambiar_nombre(self, nuevo_nombre: str):
        # Lógica de negocio para cambiar nombre
        ...

    def desactivar(self):
        # Lógica de negocio para desactivar
        ...

@dataclass
class Usuario(Entidad, AgregacionRaiz):
    nombre: Nombre = field(default_factory=Nombre)
    email: Email = field(default_factory=Email)
    metodos_pago: list[MetodoPago] = field(default_factory=list)

@dataclass
class ClienteNatural(Usuario):
    cedula: Cedula = field(default_factory=Cedula)
    fecha_nacimiento: datetime = field(default_factory=datetime)

@dataclass
class ClienteEmpresa(Usuario):
    rut: Rut = field(default_factory=Rut)
    fecha_constitucion: datetime = field(default_factory=datetime)
