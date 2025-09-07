"""Mapeadores para la capa de aplicación del dominio de cliente

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre DTOs de aplicación y entidades de dominio

"""

from datetime import datetime
from aeroalpes.seedwork.aplicacion.dto import Mapeador as AppMap
from aeroalpes.seedwork.dominio.repositorios import Mapeador as RepMap
from aeroalpes.modulos.cliente.dominio.entidades import Usuario, ClienteNatural, ClienteEmpresa, MetodoPago
from aeroalpes.modulos.cliente.dominio.objetos_valor import Nombre, Email, Cedula, Rut, TipoPago, TokenSeguridad, DatosOfuscados
from .dto import (
    UsuarioDTO, ClienteNaturalDTO, ClienteEmpresaDTO, MetodoPagoDTO
)

class MapeadorUsuarioDTOJson(AppMap):
    """Mapeador para convertir entre datos externos (JSON) y DTOs de aplicación"""
    
    def externo_a_dto(self, externo: dict) -> UsuarioDTO:
        """Convierte datos externos (JSON/dict) a DTO de aplicación"""
        
        # Mapear métodos de pago
        metodos_pago_dto = []
        for metodo_data in externo.get('metodos_pago', []):
            metodo_dto = MetodoPagoDTO(
                id=metodo_data.get('id', ''),
                tipo=metodo_data.get('tipo', ''),
                nombre=metodo_data.get('nombre', ''),
                token_seguridad=metodo_data.get('token_seguridad', ''),
                datos_ofuscados=metodo_data.get('datos_ofuscados', ''),
                fecha_creacion=metodo_data.get('fecha_creacion', ''),
                fecha_actualizacion=metodo_data.get('fecha_actualizacion', '')
            )
            metodos_pago_dto.append(metodo_dto)
        
        # Determinar tipo de usuario y crear DTO apropiado
        tipo_usuario = externo.get('tipo_usuario', 'natural')
        
        if tipo_usuario == 'natural':
            return ClienteNaturalDTO(
                id=externo.get('id', ''),
                tipo_usuario=tipo_usuario,
                nombre=externo.get('nombre', ''),
                email=externo.get('email', ''),
                cedula=externo.get('cedula', ''),
                fecha_nacimiento=externo.get('fecha_nacimiento', ''),
                fecha_creacion=externo.get('fecha_creacion', ''),
                fecha_actualizacion=externo.get('fecha_actualizacion', ''),
                metodos_pago=metodos_pago_dto
            )
        elif tipo_usuario == 'empresa':
            return ClienteEmpresaDTO(
                id=externo.get('id', ''),
                tipo_usuario=tipo_usuario,
                nombre=externo.get('nombre', ''),
                email=externo.get('email', ''),
                rut=externo.get('rut', ''),
                fecha_constitucion=externo.get('fecha_constitucion', ''),
                fecha_creacion=externo.get('fecha_creacion', ''),
                fecha_actualizacion=externo.get('fecha_actualizacion', ''),
                metodos_pago=metodos_pago_dto
            )
        else:
            return UsuarioDTO(
                id=externo.get('id', ''),
                tipo_usuario=tipo_usuario,
                nombre=externo.get('nombre', ''),
                email=externo.get('email', ''),
                fecha_creacion=externo.get('fecha_creacion', ''),
                fecha_actualizacion=externo.get('fecha_actualizacion', ''),
                metodos_pago=metodos_pago_dto
            )
    
    def dto_a_externo(self, dto: UsuarioDTO) -> dict:
        """Convierte DTO de aplicación a formato externo (dict/JSON)"""
        
        # Mapear métodos de pago
        metodos_pago_dict = []
        for metodo in dto.metodos_pago:
            metodo_dict = {
                'id': metodo.id,
                'tipo': metodo.tipo,
                'nombre': metodo.nombre,
                'token_seguridad': metodo.token_seguridad,
                'datos_ofuscados': metodo.datos_ofuscados,
                'fecha_creacion': metodo.fecha_creacion,
                'fecha_actualizacion': metodo.fecha_actualizacion
            }
            metodos_pago_dict.append(metodo_dict)
        
        # Datos base del usuario
        result = {
            'id': dto.id,
            'tipo_usuario': dto.tipo_usuario,
            'nombre': dto.nombre,
            'email': dto.email,
            'fecha_creacion': dto.fecha_creacion,
            'fecha_actualizacion': dto.fecha_actualizacion,
            'metodos_pago': metodos_pago_dict
        }
        
        # Agregar campos específicos según el tipo
        if isinstance(dto, ClienteNaturalDTO):
            result.update({
                'cedula': dto.cedula,
                'fecha_nacimiento': dto.fecha_nacimiento
            })
        elif isinstance(dto, ClienteEmpresaDTO):
            result.update({
                'rut': dto.rut,
                'fecha_constitucion': dto.fecha_constitucion
            })
        
        return result

class MapeadorUsuario(RepMap):
    """Mapeador para convertir entre DTOs de aplicación y entidades de dominio"""
    
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'
    
    def obtener_tipo(self) -> type:
        return Usuario.__class__
    
    def entidad_a_dto(self, entidad: Usuario) -> UsuarioDTO:
        """Convierte entidad de dominio a DTO de aplicación"""
        
        # Mapear métodos de pago
        metodos_pago_dto = []
        for metodo in entidad.metodos_pago:
            metodo_dto = MetodoPagoDTO(
                id=str(metodo.id),
                tipo=metodo.tipo.tipo if metodo.tipo else '',
                nombre=metodo.nombre,
                token_seguridad=metodo.token_seguridad.token if metodo.token_seguridad else '',
                datos_ofuscados=metodo.datos_ofuscados.datos if hasattr(metodo, 'datos_ofuscados') and metodo.datos_ofuscados else '',
                fecha_creacion=metodo.fecha_creacion.strftime(self._FORMATO_FECHA) if metodo.fecha_creacion else '',
                fecha_actualizacion=metodo.fecha_actualizacion.strftime(self._FORMATO_FECHA) if metodo.fecha_actualizacion else ''
            )
            metodos_pago_dto.append(metodo_dto)
        
        # Determinar tipo y crear DTO apropiado
        if isinstance(entidad, ClienteNatural):
            return ClienteNaturalDTO(
                id=str(entidad.id),
                tipo_usuario='natural',
                nombre=entidad.nombre.nombre if entidad.nombre else '',
                email=entidad.email.email if entidad.email else '',
                cedula=entidad.cedula.cedula if entidad.cedula else '',
                fecha_nacimiento=entidad.fecha_nacimiento.strftime(self._FORMATO_FECHA) if entidad.fecha_nacimiento else '',
                fecha_creacion=entidad.fecha_creacion.strftime(self._FORMATO_FECHA) if entidad.fecha_creacion else '',
                fecha_actualizacion=entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA) if entidad.fecha_actualizacion else '',
                metodos_pago=metodos_pago_dto
            )
        elif isinstance(entidad, ClienteEmpresa):
            return ClienteEmpresaDTO(
                id=str(entidad.id),
                tipo_usuario='empresa',
                nombre=entidad.nombre.nombre if entidad.nombre else '',
                email=entidad.email.email if entidad.email else '',
                rut=entidad.rut.rut if entidad.rut else '',
                fecha_constitucion=entidad.fecha_constitucion.strftime(self._FORMATO_FECHA) if entidad.fecha_constitucion else '',
                fecha_creacion=entidad.fecha_creacion.strftime(self._FORMATO_FECHA) if entidad.fecha_creacion else '',
                fecha_actualizacion=entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA) if entidad.fecha_actualizacion else '',
                metodos_pago=metodos_pago_dto
            )
        else:
            return UsuarioDTO(
                id=str(entidad.id),
                tipo_usuario='base',
                nombre=entidad.nombre.nombre if entidad.nombre else '',
                email=entidad.email.email if entidad.email else '',
                fecha_creacion=entidad.fecha_creacion.strftime(self._FORMATO_FECHA) if entidad.fecha_creacion else '',
                fecha_actualizacion=entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA) if entidad.fecha_actualizacion else '',
                metodos_pago=metodos_pago_dto
            )
    
    def dto_a_entidad(self, dto: UsuarioDTO) -> Usuario:
        """Convierte DTO de aplicación a entidad de dominio"""
        
        # Mapear métodos de pago
        metodos_pago = []
        for metodo_dto in dto.metodos_pago:
            metodo = MetodoPago()
            metodo.id = metodo_dto.id
            metodo.tipo = TipoPago(metodo_dto.tipo) if metodo_dto.tipo else TipoPago()
            metodo.nombre = metodo_dto.nombre
            metodo.token_seguridad = TokenSeguridad(metodo_dto.token_seguridad) if metodo_dto.token_seguridad else TokenSeguridad()
            if metodo_dto.datos_ofuscados:
                metodo.datos_ofuscados = DatosOfuscados(metodo_dto.datos_ofuscados)
            metodo.fecha_creacion = datetime.strptime(metodo_dto.fecha_creacion, self._FORMATO_FECHA) if metodo_dto.fecha_creacion else datetime.now()
            metodo.fecha_actualizacion = datetime.strptime(metodo_dto.fecha_actualizacion, self._FORMATO_FECHA) if metodo_dto.fecha_actualizacion else datetime.now()
            metodos_pago.append(metodo)
        
        # Crear entidad según tipo
        if isinstance(dto, ClienteNaturalDTO) or dto.tipo_usuario == 'natural':
            entidad = ClienteNatural()
            entidad.cedula = Cedula(dto.cedula) if hasattr(dto, 'cedula') and dto.cedula else Cedula()
            entidad.fecha_nacimiento = datetime.strptime(dto.fecha_nacimiento, self._FORMATO_FECHA) if hasattr(dto, 'fecha_nacimiento') and dto.fecha_nacimiento else datetime.now()
        elif isinstance(dto, ClienteEmpresaDTO) or dto.tipo_usuario == 'empresa':
            entidad = ClienteEmpresa()
            entidad.rut = Rut(dto.rut) if hasattr(dto, 'rut') and dto.rut else Rut()
            entidad.fecha_constitucion = datetime.strptime(dto.fecha_constitucion, self._FORMATO_FECHA) if hasattr(dto, 'fecha_constitucion') and dto.fecha_constitucion else datetime.now()
        else:
            entidad = Usuario()
        
        # Propiedades comunes
        entidad.id = dto.id
        entidad.nombre = Nombre(dto.nombre) if dto.nombre else Nombre()
        entidad.email = Email(dto.email) if dto.email else Email()
        entidad.metodos_pago = metodos_pago
        entidad.fecha_creacion = datetime.strptime(dto.fecha_creacion, self._FORMATO_FECHA) if dto.fecha_creacion else datetime.now()
        entidad.fecha_actualizacion = datetime.strptime(dto.fecha_actualizacion, self._FORMATO_FECHA) if dto.fecha_actualizacion else datetime.now()
        
        return entidad
