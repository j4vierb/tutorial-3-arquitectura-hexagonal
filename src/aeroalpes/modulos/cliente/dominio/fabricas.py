""" Fábricas para la creación de objetos del dominio de cliente

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de cliente

"""

from .entidades import Usuario, MetodoPago
from .reglas import NombresYApellidosValidos
from .excepciones import TipoObjetoNoExisteEnDominioClienteExcepcion
from aeroalpes.seedwork.dominio.repositorios import Mapeador
from aeroalpes.seedwork.dominio.fabricas import Fabrica
from aeroalpes.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaUsuario(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            # Convertir entidad de dominio a DTO
            return mapeador.entidad_a_dto(obj)
        else:
            # Convertir DTO a entidad de dominio
            usuario: Usuario = mapeador.dto_a_entidad(obj)

            # Validar reglas de negocio
            self.validar_regla(NombresYApellidosValidos(usuario))
            # Aquí puedes agregar más validaciones específicas
            
            return usuario

@dataclass
class _FabricaMetodoPago(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            # Convertir entidad de dominio a DTO
            return mapeador.entidad_a_dto(obj)
        else:
            # Convertir DTO a entidad de dominio
            metodo_pago: MetodoPago = mapeador.dto_a_entidad(obj)
            
            # Aquí se pueden agregar validaciones específicas para métodos de pago
            
            return metodo_pago

@dataclass
class FabricaCliente(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        
        # Nota: Aquí se aplicó el patrón Factory Method
        # La fábrica principal delega a fábricas específicas según el tipo de objeto
        
        if isinstance(obj, Usuario) or (hasattr(obj, 'tipo_usuario') and obj.tipo_usuario in ['natural', 'empresa', 'base']):
            fabrica_usuario = _FabricaUsuario()
            return fabrica_usuario.crear_objeto(obj, mapeador)
        elif isinstance(obj, MetodoPago) or (hasattr(obj, 'tipo') and hasattr(obj, 'token_seguridad')):
            fabrica_metodo_pago = _FabricaMetodoPago()
            return fabrica_metodo_pago.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioClienteExcepcion()
