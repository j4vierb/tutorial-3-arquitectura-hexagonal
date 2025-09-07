# Tutorial 3 - Arquitectura Hexagonal

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&repo=MISW4406/tutorial-3-arquitectura-hexagonal) 

Repositorio con código base para el desarrollo de una arquitectura hexagonal siguiendo los principios y patrones de DDD.

## Revisar en detalle

- `cliente/infraestructura/excepciones.py`: Excepciones de la capa de infraestructura para cliente. Fabrica y repositorio. 
- `cliente/infraestructura/fabricas.py`: Crear objetos de cliente para la capa de infraestructura. 
- `cliente/infraestructura/mapeadores.py`: Mapeadores capa de dominio del cliente
- `cliente/infraestructura/repositorios.py`: Implementaciones de los repositorios de dominio. 
- `cliente/infraestructura/dto.py`: DTOs (modelos anémicos) de la infraestructura de cliente. Un DTO en esta capa es un registro en la base de datos.


- `cliente/dominio/fabricas.py`: crear objetos complejos del cominio de cliente. 
- `cliente/dominio/excepciones.py`: Excepciones propias del dominio de cliente. Tablas en base de datos.

- `cliente/aplicacion/dto.py`: Los DTOs de esta capa son JSON a los DTOs de esta capa. 
- `cliente/aplicacion/mapeadores.py`: Clases para convertir de DTOs de esta capa a JSON y viceversa. 
- `cliente/aplicacion/servicios.py`: Reune las operaciones CRUD, validaciones de reglas de negocio y persistencia en BD. Casi que un orquestador entre todos los componentes que ya hemos trabajado. 

## Arquitectura

<img width="2746" height="450" alt="3" src="https://github.com/user-attachments/assets/14822685-fbe3-475f-a880-45c3ee3e74c9" />

## Estructura del proyecto

El repositorio en su raíz está estructurado de la siguiente forma:

- **.github**: Directorio donde se localizan templates para Github y los CI/CD workflows 
- **.devcontainer/devcontainer.json**: Archivo que define las tareas/pasos a ejecutar para configurar su workspace en Github Codespaces.
- **src**: En este directorio encuentra el código fuente para AeroAlpes. En la siguiente sección se explica un poco mejor la estructura del mismo ([link](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure%3E) para más información)
- **tests**: Directorio con todos los archivos de prueba, tanto unitarios como de integración. Sigue el estándar [recomendado por pytest](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html) y usado por [boto](https://github.com/boto/boto).
- **.gitignore**: Archivo con la definición de archivos que se deben ignorar en el repositorio GIT
- **README.md**: El archivo que está leyendo :)
- **requirements.txt**: Archivo con los requerimientos para el correcto funcionamiento del proyecto (librerias Python)


## Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/aeroalpes/api run
```

Siempre puede ejecutarlo en modo DEBUG:

```bash
flask --app src/aeroalpes/api --debug run
```


## Request de ejemplo

Los siguientes JSON pueden ser usados para probar el API:

### Reservar

- **Endpoint**: `/vuelos/reserva`
- **Método**: `POST`
- **Headers**: `Content-Type='aplication/json'`

```json
{
    "itinerarios": [
        {
            "odos": [
                {
                    "segmentos": [
                        {
                            "legs": [
                                {
                                    "fecha_salida": "2022-11-22T13:10:00Z",
                                    "fecha_llegada": "2022-11-22T15:10:00Z",
                                    "destino": {
                                        "codigo": "JFK",
                                        "nombre": "John F. Kennedy International Airport"
                                    },
                                    "origen": {
                                        "codigo": "BOG",
                                        "nombre": "El Dorado - Bogotá International Airport (BOG)"
                                    }

                                }
                            ]
                        }
                    ]
                }

            ]
        }
    ]
}
```

### Ver Reserva(s)

- **Endpoint**: `/vuelos/reserva/{id}`
- **Método**: `GET`
- **Headers**: `Content-Type='aplication/json'`

## Endpoints de Cliente

Los siguientes endpoints están disponibles para gestión de clientes:

### Crear Usuario

- **Endpoint**: `/cliente/usuarios`
- **Método**: `POST`
- **Headers**: `Content-Type='application/json'`

**Cliente Natural:**
```json
{
    "tipo_usuario": "natural",
    "nombre": "Juan Pérez",
    "email": "juan.perez@example.com",
    "cedula": "12345678",
    "fecha_nacimiento": "1990-05-15T00:00:00Z",
    "metodos_pago": [
        {
            "tipo": "CREDITO",
            "nombre": "Tarjeta Principal",
            "token_seguridad": "tok_123456789",
            "datos_ofuscados": "****1234"
        }
    ]
}
```

**Cliente Empresa:**
```json
{
    "tipo_usuario": "empresa",
    "nombre": "Empresa ABC S.A.S",
    "email": "contacto@empresa-abc.com",
    "rut": "900123456",
    "fecha_constitucion": "2020-01-15T00:00:00Z",
    "metodos_pago": [
        {
            "tipo": "DEBITO",
            "nombre": "Cuenta Empresarial",
            "token_seguridad": "tok_987654321",
            "datos_ofuscados": "****5678"
        }
    ]
}
```

### Obtener Usuario por ID

- **Endpoint**: `/cliente/usuarios/{id}`
- **Método**: `GET`
- **Headers**: `Content-Type='application/json'`

### Obtener Usuario por Email

- **Endpoint**: `/cliente/usuarios/email/{email}`
- **Método**: `GET`
- **Headers**: `Content-Type='application/json'`

### Obtener Todos los Usuarios

- **Endpoint**: `/cliente/usuarios`
- **Método**: `GET`
- **Headers**: `Content-Type='application/json'`

### Actualizar Usuario

- **Endpoint**: `/cliente/usuarios/{id}`
- **Método**: `PUT`
- **Headers**: `Content-Type='application/json'`

```json
{
    "nombre": "Juan Carlos Pérez",
    "email": "juan.carlos@example.com",
    "metodos_pago": [
        {
            "tipo": "CREDITO",
            "nombre": "Nueva Tarjeta",
            "token_seguridad": "tok_nuevo_123",
            "datos_ofuscados": "****9999"
        }
    ]
}
```

### Eliminar Usuario

- **Endpoint**: `/cliente/usuarios/{id}`
- **Método**: `DELETE`
- **Headers**: `Content-Type='application/json'`

### Health Check del Módulo Cliente

- **Endpoint**: `/cliente/health`
- **Método**: `GET`

## Ejecutar pruebas

```bash
coverage run -m pytest
```

# Ver reporte de covertura
```bash
coverage report
```
## Diagrama con Flujo Crear Reserva
A continuación un diagrama mostrando como es el flujo de un request de reservar o crear reserva  a través de las diferentes capas:

![image](https://github.com/user-attachments/assets/70b93bd8-b799-4f96-8a0f-708341d91187)
