"""DTOs para la capa de infrastructura del dominio de clientes

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio del cliente

"""

from aeroalpes.config.db import db
from sqlalchemy.orm import relationship
import uuid

# Tabla intermedia para la relación muchos a muchos entre usuarios y métodos de pago
usuarios_metodos_pago = db.Table(
    "usuarios_metodos_pago",
    db.Model.metadata,
    db.Column("usuario_id", db.String, db.ForeignKey("usuarios.id")),
    db.Column("metodo_pago_id", db.String, db.ForeignKey("metodos_pago.id"))
)

class MetodoPago(db.Model):
    __tablename__ = "metodos_pago"
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tipo = db.Column(db.String, nullable=False)
    nombre = db.Column(db.String, nullable=False)
    token_seguridad = db.Column(db.String, nullable=False)
    datos_ofuscados = db.Column(db.String, nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)

class Usuario(db.Model):
    __tablename__ = "usuarios"
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tipo_usuario = db.Column(db.String, nullable=False)  # 'natural' o 'empresa'
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    
    # Campos específicos para ClienteNatural
    cedula = db.Column(db.String, nullable=True)
    fecha_nacimiento = db.Column(db.DateTime, nullable=True)
    
    # Campos específicos para ClienteEmpresa  
    rut = db.Column(db.String, nullable=True)
    fecha_constitucion = db.Column(db.DateTime, nullable=True)
    
    # Relación con métodos de pago
    metodos_pago = relationship("MetodoPago", secondary=usuarios_metodos_pago, backref="usuarios")
