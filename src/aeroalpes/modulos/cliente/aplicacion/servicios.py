"""Servicios de aplicación para el dominio de cliente

En este archivo usted encontrará los diferentes servicios de aplicación
para coordinar casos de uso del dominio de cliente

"""

from uuid import UUID
from aeroalpes.modulos.cliente.dominio.entidades import Usuario
from aeroalpes.modulos.cliente.dominio.fabricas import FabricaCliente
from aeroalpes.modulos.cliente.infraestructura.fabricas import FabricaRepositorio
from aeroalpes.modulos.cliente.dominio.repositorios import RepositorioUsuarios
from aeroalpes.seedwork.aplicacion.servicios import Servicio

from .dto import UsuarioDTO, ClienteNaturalDTO, ClienteEmpresaDTO, CrearUsuarioDTO, ActualizarUsuarioDTO
from .mapeadores import MapeadorUsuario, MapeadorUsuarioDTOJson


class ServicioUsuario(Servicio):
    """Servicio de aplicación para gestionar usuarios (casos de uso)"""

    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_cliente: FabricaCliente = FabricaCliente()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_cliente(self):
        return self._fabrica_cliente

    def crear_usuario(self, usuario_dto: CrearUsuarioDTO) -> UsuarioDTO:
        """Caso de uso: Crear un nuevo usuario"""
        
        # Convertir DTO de creación a DTO estándar
        if usuario_dto.tipo_usuario == 'natural':
            dto_usuario = ClienteNaturalDTO(
                tipo_usuario=usuario_dto.tipo_usuario,
                nombre=usuario_dto.nombre,
                email=usuario_dto.email,
                cedula=usuario_dto.cedula,
                fecha_nacimiento=usuario_dto.fecha_nacimiento,
                metodos_pago=usuario_dto.metodos_pago
            )
        elif usuario_dto.tipo_usuario == 'empresa':
            dto_usuario = ClienteEmpresaDTO(
                tipo_usuario=usuario_dto.tipo_usuario,
                nombre=usuario_dto.nombre,
                email=usuario_dto.email,
                rut=usuario_dto.rut,
                fecha_constitucion=usuario_dto.fecha_constitucion,
                metodos_pago=usuario_dto.metodos_pago
            )
        else:
            dto_usuario = UsuarioDTO(
                tipo_usuario=usuario_dto.tipo_usuario,
                nombre=usuario_dto.nombre,
                email=usuario_dto.email,
                metodos_pago=usuario_dto.metodos_pago
            )

        # Crear entidad de dominio usando la fábrica (aplica validaciones)
        usuario: Usuario = self.fabrica_cliente.crear_objeto(dto_usuario, MapeadorUsuario())

        # Persistir usando el repositorio
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioUsuarios)
        repositorio.agregar(usuario)

        # Retornar DTO de respuesta
        return self.fabrica_cliente.crear_objeto(usuario, MapeadorUsuario())

    def obtener_usuario_por_id(self, id: UUID) -> UsuarioDTO:
        """Caso de uso: Obtener usuario por ID"""
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioUsuarios)
        usuario = repositorio.obtener_por_id(id)
        
        # Convertir entidad a DTO usando la fábrica
        return self.fabrica_cliente.crear_objeto(usuario, MapeadorUsuario())

    def obtener_usuario_por_email(self, email: str) -> UsuarioDTO:
        """Caso de uso: Obtener usuario por email"""
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioUsuarios)
        usuario = repositorio.obtener_por_email(email)
        
        # Convertir entidad a DTO usando la fábrica
        return self.fabrica_cliente.crear_objeto(usuario, MapeadorUsuario())

    def obtener_todos_los_usuarios(self) -> list[UsuarioDTO]:
        """Caso de uso: Obtener todos los usuarios"""
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioUsuarios)
        usuarios = repositorio.obtener_todos()
        
        # Convertir entidades a DTOs
        usuarios_dto = []
        for usuario in usuarios:
            usuario_dto = self.fabrica_cliente.crear_objeto(usuario, MapeadorUsuario())
            usuarios_dto.append(usuario_dto)
        
        return usuarios_dto

    def actualizar_usuario(self, usuario_dto: ActualizarUsuarioDTO) -> UsuarioDTO:
        """Caso de uso: Actualizar un usuario existente"""
        
        # Obtener usuario existente
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioUsuarios)
        usuario_existente = repositorio.obtener_por_id(UUID(usuario_dto.id))
        
        # Actualizar campos modificables
        if usuario_dto.nombre:
            from aeroalpes.modulos.cliente.dominio.objetos_valor import Nombre
            usuario_existente.nombre = Nombre(usuario_dto.nombre)
        
        if usuario_dto.email:
            from aeroalpes.modulos.cliente.dominio.objetos_valor import Email
            usuario_existente.email = Email(usuario_dto.email)
        
        if usuario_dto.metodos_pago:
            # Convertir DTOs a entidades de métodos de pago
            from aeroalpes.modulos.cliente.dominio.entidades import MetodoPago
            from aeroalpes.modulos.cliente.dominio.objetos_valor import TipoPago, TokenSeguridad, DatosOfuscados
            from datetime import datetime
            
            metodos_pago = []
            for metodo_dto in usuario_dto.metodos_pago:
                metodo = MetodoPago()
                metodo.tipo = TipoPago(metodo_dto.tipo) if metodo_dto.tipo else TipoPago()
                metodo.nombre = metodo_dto.nombre
                metodo.token_seguridad = TokenSeguridad(metodo_dto.token_seguridad) if metodo_dto.token_seguridad else TokenSeguridad()
                if metodo_dto.datos_ofuscados:
                    metodo.datos_ofuscados = DatosOfuscados(metodo_dto.datos_ofuscados)
                metodo.fecha_actualizacion = datetime.now()
                metodos_pago.append(metodo)
            
            usuario_existente.metodos_pago = metodos_pago
        
        # Actualizar timestamp
        from datetime import datetime
        usuario_existente.fecha_actualizacion = datetime.now()
        
        # Persistir cambios
        repositorio.actualizar(usuario_existente)
        
        # Retornar DTO actualizado
        return self.fabrica_cliente.crear_objeto(usuario_existente, MapeadorUsuario())

    def eliminar_usuario(self, id: UUID) -> bool:
        """Caso de uso: Eliminar un usuario"""
        try:
            repositorio = self.fabrica_repositorio.crear_objeto(RepositorioUsuarios)
            repositorio.eliminar(id)
            return True
        except Exception:
            return False

    def crear_usuario_desde_json(self, usuario_json: dict) -> UsuarioDTO:
        """Caso de uso: Crear usuario desde datos JSON externos"""
        
        # Mapear JSON a DTO usando el mapeador externo
        mapeador_json = MapeadorUsuarioDTOJson()
        usuario_dto = mapeador_json.externo_a_dto(usuario_json)
        
        # Crear entidad de dominio
        usuario: Usuario = self.fabrica_cliente.crear_objeto(usuario_dto, MapeadorUsuario())
        
        # Persistir
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioUsuarios)
        repositorio.agregar(usuario)
        
        # Retornar DTO
        return self.fabrica_cliente.crear_objeto(usuario, MapeadorUsuario())
