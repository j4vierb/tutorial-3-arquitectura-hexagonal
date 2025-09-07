""" Mapeadores para la capa de infrastructura del dominio de cliente

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from datetime import datetime
from aeroalpes.seedwork.dominio.repositorios import Mapeador
from aeroalpes.modulos.cliente.dominio.entidades import Usuario, ClienteNatural, ClienteEmpresa, MetodoPago
from aeroalpes.modulos.cliente.dominio.objetos_valor import Nombre, Email, Cedula, Rut, TipoPago, TokenSeguridad, DatosOfuscados
from .dto import Usuario as UsuarioDTO, MetodoPago as MetodoPagoDTO

class MapeadorUsuario(Mapeador):
    
    def obtener_tipo(self) -> type:
        return Usuario.__class__
    
    def entidad_a_dto(self, entidad: Usuario) -> UsuarioDTO:
        """Convierte una entidad de dominio a DTO"""
        
        # Determinar tipo de usuario
        if isinstance(entidad, ClienteNatural):
            tipo_usuario = 'natural'
            cedula = entidad.cedula.cedula if entidad.cedula else None
            fecha_nacimiento = entidad.fecha_nacimiento
            rut = None
            fecha_constitucion = None
        elif isinstance(entidad, ClienteEmpresa):
            tipo_usuario = 'empresa'
            cedula = None
            fecha_nacimiento = None
            rut = entidad.rut.rut if entidad.rut else None
            fecha_constitucion = entidad.fecha_constitucion
        else:
            tipo_usuario = 'base'
            cedula = None
            fecha_nacimiento = None
            rut = None
            fecha_constitucion = None
        
        # Mapear métodos de pago
        metodos_pago_dto = []
        for metodo in entidad.metodos_pago:
            metodo_dto = MetodoPagoDTO()
            metodo_dto.id = str(metodo.id)
            metodo_dto.tipo = metodo.tipo.tipo if metodo.tipo else None
            metodo_dto.nombre = metodo.nombre
            metodo_dto.token_seguridad = metodo.token_seguridad.token if metodo.token_seguridad else None
            metodo_dto.datos_ofuscados = metodo.datos_ofuscados.datos if hasattr(metodo, 'datos_ofuscados') and metodo.datos_ofuscados else None
            metodo_dto.fecha_creacion = metodo.fecha_creacion
            metodo_dto.fecha_actualizacion = metodo.fecha_actualizacion
            metodos_pago_dto.append(metodo_dto)
        
        # Crear DTO principal
        usuario_dto = UsuarioDTO()
        usuario_dto.id = str(entidad.id)
        usuario_dto.tipo_usuario = tipo_usuario
        usuario_dto.nombre = entidad.nombre.nombre if entidad.nombre else None
        usuario_dto.email = entidad.email.email if entidad.email else None
        usuario_dto.cedula = cedula
        usuario_dto.fecha_nacimiento = fecha_nacimiento
        usuario_dto.rut = rut
        usuario_dto.fecha_constitucion = fecha_constitucion
        usuario_dto.fecha_creacion = entidad.fecha_creacion
        usuario_dto.fecha_actualizacion = entidad.fecha_actualizacion
        usuario_dto.metodos_pago = metodos_pago_dto
        
        return usuario_dto
    
    def dto_a_entidad(self, dto: UsuarioDTO) -> Usuario:
        """Convierte un DTO a entidad de dominio"""
        
        # Mapear métodos de pago
        metodos_pago = []
        for metodo_dto in dto.metodos_pago if dto.metodos_pago else []:
            metodo = MetodoPago()
            metodo.id = metodo_dto.id
            metodo.tipo = TipoPago(metodo_dto.tipo) if metodo_dto.tipo else TipoPago()
            metodo.nombre = metodo_dto.nombre
            metodo.token_seguridad = TokenSeguridad(metodo_dto.token_seguridad) if metodo_dto.token_seguridad else TokenSeguridad()
            if metodo_dto.datos_ofuscados:
                metodo.datos_ofuscados = DatosOfuscados(metodo_dto.datos_ofuscados)
            metodo.fecha_creacion = metodo_dto.fecha_creacion
            metodo.fecha_actualizacion = metodo_dto.fecha_actualizacion
            metodos_pago.append(metodo)
        
        # Crear entidad según tipo
        if dto.tipo_usuario == 'natural':
            entidad = ClienteNatural()
            entidad.cedula = Cedula(dto.cedula) if dto.cedula else Cedula()
            entidad.fecha_nacimiento = dto.fecha_nacimiento if dto.fecha_nacimiento else datetime.now()
        elif dto.tipo_usuario == 'empresa':
            entidad = ClienteEmpresa()
            entidad.rut = Rut(dto.rut) if dto.rut else Rut()
            entidad.fecha_constitucion = dto.fecha_constitucion if dto.fecha_constitucion else datetime.now()
        else:
            entidad = Usuario()
        
        # Propiedades comunes
        entidad.id = dto.id
        entidad.nombre = Nombre(dto.nombre) if dto.nombre else Nombre()
        entidad.email = Email(dto.email) if dto.email else Email()
        entidad.metodos_pago = metodos_pago
        entidad.fecha_creacion = dto.fecha_creacion
        entidad.fecha_actualizacion = dto.fecha_actualizacion
        
        return entidad

class MapeadorMetodoPago(Mapeador):
    
    def obtener_tipo(self) -> type:
        return MetodoPago.__class__
    
    def entidad_a_dto(self, entidad: MetodoPago) -> MetodoPagoDTO:
        """Convierte una entidad MetodoPago a DTO"""
        dto = MetodoPagoDTO()
        dto.id = str(entidad.id)
        dto.tipo = entidad.tipo.tipo if entidad.tipo else None
        dto.nombre = entidad.nombre
        dto.token_seguridad = entidad.token_seguridad.token if entidad.token_seguridad else None
        dto.datos_ofuscados = entidad.datos_ofuscados.datos if hasattr(entidad, 'datos_ofuscados') and entidad.datos_ofuscados else None
        dto.fecha_creacion = entidad.fecha_creacion
        dto.fecha_actualizacion = entidad.fecha_actualizacion
        return dto
    
    def dto_a_entidad(self, dto: MetodoPagoDTO) -> MetodoPago:
        """Convierte un DTO a entidad MetodoPago"""
        entidad = MetodoPago()
        entidad.id = dto.id
        entidad.tipo = TipoPago(dto.tipo) if dto.tipo else TipoPago()
        entidad.nombre = dto.nombre
        entidad.token_seguridad = TokenSeguridad(dto.token_seguridad) if dto.token_seguridad else TokenSeguridad()
        if dto.datos_ofuscados:
            entidad.datos_ofuscados = DatosOfuscados(dto.datos_ofuscados)
        entidad.fecha_creacion = dto.fecha_creacion
        entidad.fecha_actualizacion = dto.fecha_actualizacion
        return entidad
