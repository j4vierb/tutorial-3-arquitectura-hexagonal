""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de cliente

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de cliente

"""

from dataclasses import dataclass

from aeroalpes.modulos.cliente.dominio.repositorios import RepositorioUsuarios
from aeroalpes.seedwork.dominio.fabricas import Fabrica
from aeroalpes.seedwork.dominio.repositorios import Repositorio

from .excepciones import ExcepcionFabrica
from .repositorios import RepositorioUsuariosSQLite


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioUsuarios:
            return RepositorioUsuariosSQLite()
        else:
            raise ExcepcionFabrica(f"No existe fábrica para el tipo {obj}")
