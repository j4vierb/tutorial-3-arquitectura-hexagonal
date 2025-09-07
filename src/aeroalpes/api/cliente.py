"""API endpoints para el módulo de cliente

En este archivo encontrará los endpoints REST para gestión de clientes

"""

import aeroalpes.seedwork.presentacion.api as api
import json
from uuid import UUID
from aeroalpes.modulos.cliente.aplicacion.servicios import ServicioUsuario
from aeroalpes.modulos.cliente.aplicacion.dto import ActualizarUsuarioDTO
from aeroalpes.modulos.cliente.aplicacion.mapeadores import MapeadorUsuarioDTOJson
from aeroalpes.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request, Response

bp = api.crear_blueprint('cliente', '/cliente')

@bp.route('/usuarios', methods=('POST',))
def crear_usuario():
    """Endpoint para crear un nuevo usuario"""
    try:
        usuario_dict = request.json
        
        # Llamar al servicio de aplicación directamente con JSON
        servicio_usuario = ServicioUsuario()
        usuario_creado = servicio_usuario.crear_usuario_desde_json(usuario_dict)
        
        # Convertir respuesta a formato externo
        mapeador_json = MapeadorUsuarioDTOJson()
        resultado = mapeador_json.dto_a_externo(usuario_creado)
        
        return Response(
            json.dumps(resultado), 
            status=201, 
            mimetype='application/json'
        )
        
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))), 
            status=400, 
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            json.dumps(dict(error=f"Error interno: {str(e)}")), 
            status=500, 
            mimetype='application/json'
        )

@bp.route('/usuarios/<id>', methods=('GET',))
def obtener_usuario_por_id(id):
    """Endpoint para obtener un usuario por ID"""
    try:
        # Convertir string a UUID
        usuario_id = UUID(id)
        
        # Llamar al servicio de aplicación
        servicio_usuario = ServicioUsuario()
        usuario_dto = servicio_usuario.obtener_usuario_por_id(usuario_id)
        
        # Convertir a formato externo
        mapeador_json = MapeadorUsuarioDTOJson()
        resultado = mapeador_json.dto_a_externo(usuario_dto)
        
        return Response(
            json.dumps(resultado), 
            status=200, 
            mimetype='application/json'
        )
        
    except ValueError:
        return Response(
            json.dumps(dict(error="ID de usuario inválido")), 
            status=400, 
            mimetype='application/json'
        )
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))), 
            status=404, 
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            json.dumps(dict(error=f"Error interno: {str(e)}")), 
            status=500, 
            mimetype='application/json'
        )

@bp.route('/usuarios', methods=('GET',))
def obtener_todos_usuarios():
    """Endpoint para obtener todos los usuarios"""
    try:
        # Llamar al servicio de aplicación
        servicio_usuario = ServicioUsuario()
        usuarios_dto = servicio_usuario.obtener_todos_los_usuarios()
        
        # Convertir a formato externo
        mapeador_json = MapeadorUsuarioDTOJson()
        resultado = []
        for usuario_dto in usuarios_dto:
            usuario_dict = mapeador_json.dto_a_externo(usuario_dto)
            resultado.append(usuario_dict)
        
        return Response(
            json.dumps(resultado), 
            status=200, 
            mimetype='application/json'
        )
        
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))), 
            status=400, 
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            json.dumps(dict(error=f"Error interno: {str(e)}")), 
            status=500, 
            mimetype='application/json'
        )

@bp.route('/usuarios/email/<email>', methods=('GET',))
def obtener_usuario_por_email(email):
    """Endpoint para obtener un usuario por email"""
    try:
        # Llamar al servicio de aplicación
        servicio_usuario = ServicioUsuario()
        usuario_dto = servicio_usuario.obtener_usuario_por_email(email)
        
        # Convertir a formato externo
        mapeador_json = MapeadorUsuarioDTOJson()
        resultado = mapeador_json.dto_a_externo(usuario_dto)
        
        return Response(
            json.dumps(resultado), 
            status=200, 
            mimetype='application/json'
        )
        
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))), 
            status=404, 
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            json.dumps(dict(error=f"Error interno: {str(e)}")), 
            status=500, 
            mimetype='application/json'
        )

@bp.route('/usuarios/<id>', methods=('PUT',))
def actualizar_usuario(id):
    """Endpoint para actualizar un usuario existente"""
    try:
        usuario_dict = request.json
        
        # Validar que el ID del path coincida con el del body (si existe)
        if 'id' in usuario_dict and usuario_dict['id'] != id:
            return Response(
                json.dumps(dict(error="El ID del path no coincide con el del body")), 
                status=400, 
                mimetype='application/json'
            )
        
        # Agregar ID al dict si no existe
        usuario_dict['id'] = id
        
        # Crear DTO de actualización
        dto_actualizacion = ActualizarUsuarioDTO(
            id=usuario_dict.get('id'),
            nombre=usuario_dict.get('nombre', ''),
            email=usuario_dict.get('email', ''),
            metodos_pago=usuario_dict.get('metodos_pago', [])
        )
        
        # Llamar al servicio de aplicación
        servicio_usuario = ServicioUsuario()
        usuario_actualizado = servicio_usuario.actualizar_usuario(dto_actualizacion)
        
        # Convertir a formato externo
        mapeador_json = MapeadorUsuarioDTOJson()
        resultado = mapeador_json.dto_a_externo(usuario_actualizado)
        
        return Response(
            json.dumps(resultado), 
            status=200, 
            mimetype='application/json'
        )
        
    except ValueError:
        return Response(
            json.dumps(dict(error="ID de usuario inválido")), 
            status=400, 
            mimetype='application/json'
        )
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))), 
            status=400, 
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            json.dumps(dict(error=f"Error interno: {str(e)}")), 
            status=500, 
            mimetype='application/json'
        )

@bp.route('/usuarios/<id>', methods=('DELETE',))
def eliminar_usuario(id):
    """Endpoint para eliminar un usuario"""
    try:
        # Convertir string a UUID
        usuario_id = UUID(id)
        
        # Llamar al servicio de aplicación
        servicio_usuario = ServicioUsuario()
        eliminado = servicio_usuario.eliminar_usuario(usuario_id)
        
        if eliminado:
            return Response(
                json.dumps(dict(message="Usuario eliminado correctamente")), 
                status=200, 
                mimetype='application/json'
            )
        else:
            return Response(
                json.dumps(dict(error="No se pudo eliminar el usuario")), 
                status=400, 
                mimetype='application/json'
            )
        
    except ValueError:
        return Response(
            json.dumps(dict(error="ID de usuario inválido")), 
            status=400, 
            mimetype='application/json'
        )
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))), 
            status=404, 
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            json.dumps(dict(error=f"Error interno: {str(e)}")), 
            status=500, 
            mimetype='application/json'
        )

@bp.route('/health', methods=('GET',))
def health_check():
    """Endpoint de health check para el módulo de cliente"""
    return Response(
        json.dumps(dict(
            status="OK", 
            module="cliente",
            message="Módulo de cliente funcionando correctamente"
        )), 
        status=200, 
        mimetype='application/json'
    )