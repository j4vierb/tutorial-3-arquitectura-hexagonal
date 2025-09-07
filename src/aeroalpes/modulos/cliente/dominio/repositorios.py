""" Interfaces para los repositorios del dominio de cliente

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de cliente

"""

from abc import ABC
from aeroalpes.seedwork.dominio.repositorios import Repositorio

class RepositorioUsuarios(Repositorio, ABC):
    """Repositorio para gestionar agregados de Usuario (ClienteNatural y ClienteEmpresa)
    
    Nota: No necesitamos repositorio separado para MetodoPago ya que es una entidad
    interna del agregado Usuario y se accede a través de él.
    """
    ...
