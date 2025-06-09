# CRM Di Paolo - Sistema de Gestión de Créditos

Este sistema permite gestionar créditos, pagos y clientes, con funcionalidades para administradores y usuarios regulares. El sistema incluye procesamiento de archivos DBF, conversión a CSV y carga de datos en una base de datos PostgreSQL.

## Requisitos Previos

- Python 3.8 o superior
- PostgreSQL
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r backend/requirements.txt
```

4. Configurar variables de entorno:
   Crear un archivo `.env` en la carpeta `backend` con las siguientes variables:

```
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
DB_NAME=crm_dipaolo
SECRET_KEY=tu_clave_secreta
```

## Configuración de la Base de Datos

1. Crear la base de datos en PostgreSQL:

```sql
CREATE DATABASE crm_dipaolo;
```

2. Ejecutar las migraciones:

```bash
cd backend
flask db upgrade
```

## Registro de Administrador

Para registrar un usuario administrador, se debe ejecutar el siguiente comando en la consola de Python:

```python
from app import app, db
from models import Usuario

with app.app_context():
    admin = Usuario(
        email="admin@ejemplo.com",
        password="contraseña_segura",
        rol="admin"
    )
    db.session.add(admin)
    db.session.commit()
```

## Autenticación

### Login

1. Realizar una petición POST a `/api/login` con las credenciales:

```json
{
  "email": "tu_email@ejemplo.com",
  "password": "tu_contraseña"
}
```

2. El sistema devolverá un token JWT que debe incluirse en las cabeceras de las peticiones subsiguientes:

```
Authorization: Bearer <token>
```

## Procesamiento de Archivos

### 1. Cargar Archivos DBF

1. Colocar los archivos DBF en la carpeta `backend/uploads/`
   - CREMAE.DBF (archivo de créditos)
   - CREPAG.DBF (archivo de pagos)

### 2. Convertir DBF a CSV

Ejecutar el script de conversión:

```bash
cd backend
python convertir.py
```

Este proceso generará tres archivos CSV en la carpeta `backend/data/`:

- creditos.csv
- pagos.csv
- clientes.csv

### 3. Cargar Datos en la Base de Datos

Ejecutar el script de carga:

```bash
cd backend
python cargar_db.py
```

Este proceso cargará los datos de los archivos CSV en las tablas correspondientes de la base de datos.

## Verificación

Para verificar que los datos se han cargado correctamente:

1. Iniciar el servidor:

```bash
cd backend
python app.py
```

2. Acceder a las rutas protegidas con el token JWT:

- `/api/creditos` - Listar créditos
- `/api/pagos` - Listar pagos
- `/api/clientes` - Listar clientes

## Estructura del Proyecto

```
backend/
├── app.py              # Aplicación principal Flask
├── auth.py             # Autenticación y autorización
├── cargar_db.py        # Script para cargar datos en la DB
├── convertir.py        # Script para convertir DBF a CSV
├── requirements.txt    # Dependencias del proyecto
├── data/              # Archivos CSV generados
├── uploads/           # Archivos DBF originales
├── models/            # Modelos de la base de datos
├── routes/            # Rutas de la API
└── utils/             # Utilidades y scripts auxiliares
```

## Notas Importantes

- Mantener segura la clave secreta (SECRET_KEY) en el archivo .env
- Realizar respaldos de la base de datos regularmente
- Verificar la integridad de los archivos DBF antes de procesarlos
- Los archivos CSV generados se sobrescriben en cada conversión
