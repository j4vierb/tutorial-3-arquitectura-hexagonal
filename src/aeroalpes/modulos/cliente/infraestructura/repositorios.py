""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infraestructura del dominio de cliente

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de cliente

"""

from uuid import UUID
from aeroalpes.config.db import db
from aeroalpes.modulos.cliente.dominio.repositorios import RepositorioUsuarios
from aeroalpes.modulos.cliente.dominio.entidades import Usuario, ClienteNatural
from aeroalpes.modulos.cliente.dominio.fabricas import FabricaCliente
from .dto import Usuario as UsuarioDTO
from .mapeadores import MapeadorUsuario
from .excepciones import ExcepcionRepositorio

class RepositorioUsuariosSQLite(RepositorioUsuarios):
    
    def __init__(self):
        self._fabrica_cliente: FabricaCliente = FabricaCliente()

    @property
    def fabrica_cliente(self):
        return self._fabrica_cliente

    def obtener_por_id(self, id: UUID) -> Usuario:
        """Obtiene un usuario por su ID"""
        try:
            usuario_dto = db.session.query(UsuarioDTO).filter_by(id=str(id)).one()
            return self.fabrica_cliente.crear_objeto(usuario_dto, MapeadorUsuario())
        except Exception as e:
            raise ExcepcionRepositorio(f"Error al obtener usuario por ID {id}: {str(e)}")

    def obtener_por_email(self, email: str) -> Usuario:
        """Obtiene un usuario por su email"""
        try:
            usuario_dto = db.session.query(UsuarioDTO).filter_by(email=email).one()
            return self.fabrica_cliente.crear_objeto(usuario_dto, MapeadorUsuario())
        except Exception as e:
            raise ExcepcionRepositorio(f"Error al obtener usuario por email {email}: {str(e)}")

    def obtener_todos(self) -> list[Usuario]:
        """Obtiene todos los usuarios - Para propósitos de demostración"""
        try:
            # Crear algunos usuarios de ejemplo para demostración
            from aeroalpes.modulos.cliente.dominio.objetos_valor import Nombre, Email, Cedula, TipoPago, TokenSeguridad
            from aeroalpes.modulos.cliente.dominio.entidades import MetodoPago
            from datetime import datetime
            
            # Usuario Natural de ejemplo
            metodo_pago = MetodoPago()
            metodo_pago.tipo = TipoPago("CREDITO")
            metodo_pago.nombre = "Tarjeta Principal"
            metodo_pago.token_seguridad = TokenSeguridad("tok_123456789")
            
            cliente_natural = ClienteNatural()
            cliente_natural.nombre = Nombre("Juan Pérez")
            cliente_natural.email = Email("juan.perez@example.com")
            cliente_natural.cedula = Cedula("12345678")
            cliente_natural.fecha_nacimiento = datetime(1990, 5, 15)
            cliente_natural.metodos_pago = [metodo_pago]
            
            return [cliente_natural]
        except Exception as e:
            raise ExcepcionRepositorio(f"Error al obtener todos los usuarios: {str(e)}")

    def agregar(self, usuario: Usuario):
        """Agrega un nuevo usuario"""
        try:
            usuario_dto = self.fabrica_cliente.crear_objeto(usuario, MapeadorUsuario())
            db.session.add(usuario_dto)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ExcepcionRepositorio(f"Error al agregar usuario: {str(e)}")

    def actualizar(self, usuario: Usuario):
        """Actualiza un usuario existente"""
        try:
            # Buscar el usuario existente
            usuario_existente = db.session.query(UsuarioDTO).filter_by(id=str(usuario.id)).one()
            
            # Mapear los nuevos datos
            usuario_dto = self.fabrica_cliente.crear_objeto(usuario, MapeadorUsuario())
            
            # Actualizar campos
            usuario_existente.nombre = usuario_dto.nombre
            usuario_existente.email = usuario_dto.email
            usuario_existente.fecha_actualizacion = usuario_dto.fecha_actualizacion
            
            if hasattr(usuario_dto, 'cedula') and usuario_dto.cedula:
                usuario_existente.cedula = usuario_dto.cedula
            if hasattr(usuario_dto, 'rut') and usuario_dto.rut:
                usuario_existente.rut = usuario_dto.rut
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ExcepcionRepositorio(f"Error al actualizar usuario: {str(e)}")

    def eliminar(self, usuario_id: UUID):
        """Elimina un usuario por su ID"""
        try:
            usuario = db.session.query(UsuarioDTO).filter_by(id=str(usuario_id)).one()
            db.session.delete(usuario)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ExcepcionRepositorio(f"Error al eliminar usuario {usuario_id}: {str(e)}")