"""DTOs para la capa de aplicación del dominio de cliente

En este archivo usted encontrará los DTOs de la capa de aplicación del dominio de cliente

"""

from dataclasses import dataclass, field
from aeroalpes.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class MetodoPagoDTO(DTO):
    id: str = field(default_factory=str)
    tipo: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    token_seguridad: str = field(default_factory=str)
    datos_ofuscados: str = field(default_factory=str)
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)

@dataclass(frozen=True)
class UsuarioDTO(DTO):
    id: str = field(default_factory=str)
    tipo_usuario: str = field(default_factory=str)  # 'natural', 'empresa'
    nombre: str = field(default_factory=str)
    email: str = field(default_factory=str)
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    metodos_pago: list[MetodoPagoDTO] = field(default_factory=list)

@dataclass(frozen=True)
class ClienteNaturalDTO(UsuarioDTO):
    cedula: str = field(default_factory=str)
    fecha_nacimiento: str = field(default_factory=str)

@dataclass(frozen=True)
class ClienteEmpresaDTO(UsuarioDTO):
    rut: str = field(default_factory=str)
    fecha_constitucion: str = field(default_factory=str)

@dataclass(frozen=True)
class CrearUsuarioDTO(DTO):
    """DTO para la creación de usuarios"""
    tipo_usuario: str  # 'natural' o 'empresa'
    nombre: str
    email: str
    cedula: str = field(default="")
    fecha_nacimiento: str = field(default="")
    rut: str = field(default="")
    fecha_constitucion: str = field(default="")
    metodos_pago: list[MetodoPagoDTO] = field(default_factory=list)

@dataclass(frozen=True)
class ActualizarUsuarioDTO(DTO):
    """DTO para la actualización de usuarios"""
    id: str
    nombre: str = field(default="")
    email: str = field(default="")
    metodos_pago: list[MetodoPagoDTO] = field(default_factory=list)
