# CRM Di Paolo - Sistema Integral de Gestión de Créditos

Este sistema permite gestionar créditos, pagos y clientes, con funcionalidades para administradores y usuarios. Incluye procesamiento de archivos DBF, conversión a CSV y carga de datos en una base de datos PostgreSQL, así como un frontend moderno en React para la visualización y administración.

---

## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Instalación y Configuración](#instalación-y-configuración)
- [Estructura del Backend](#estructura-del-backend)
- [Estructura del Frontend](#estructura-del-frontend)
- [Modelos de Datos](#modelos-de-datos)
- [Rutas y Endpoints Principales](#rutas-y-endpoints-principales)
- [Flujo de Procesamiento de Archivos](#flujo-de-procesamiento-de-archivos)
- [Autenticación y Autorización](#autenticación-y-autorización)
- [Notas de Seguridad y Buenas Prácticas](#notas-de-seguridad-y-buenas-prácticas)
- [Ejemplos de Uso de la API](#ejemplos-de-uso-de-la-api)

---

## Descripción General

CRM Di Paolo es una solución para la gestión de créditos, pagos y clientes, orientada a empresas que trabajan con financiamiento y cobranza. Permite importar datos desde sistemas legados (archivos DBF), procesarlos y visualizarlos de manera moderna y segura.

## Tecnologías Utilizadas

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-CORS, JWT, dotenv
- **Base de datos:** PostgreSQL
- **Frontend:** React, Vite, Axios, React Router, React Toastify, Chart.js

## Arquitectura del Sistema

- **Backend:** API RESTful en Flask, con rutas protegidas por JWT y roles (usuario/admin). Procesa archivos DBF, los convierte a CSV y los carga en la base de datos.
- **Frontend:** SPA en React, con autenticación, panel de métricas, carga de archivos y navegación protegida.

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd CRM_Dipaolo
```

### 2. Backend

- Crear entorno virtual y activar:
  ```bash
  python -m venv venv
  source venv/bin/activate  # En Windows: venv\Scripts\activate
  ```
- Instalar dependencias:
  ```bash
  pip install -r backend/requirements.txt
  ```
- Configurar variables de entorno en `backend/.env`:
  ```env
  DB_USER=tu_usuario
  DB_PASSWORD=tu_contraseña
  DB_HOST=localhost
  DB_PORT=5432
  DB_NAME=crm_dipaolo
  SECRET_KEY=tu_clave_secreta
  ```
- Crear la base de datos en PostgreSQL:
  ```sql
  CREATE DATABASE crm_dipaolo;
  ```
- Ejecutar migraciones:
  ```bash
  cd backend
  flask db upgrade
  ```

### 3. Frontend

- Instalar dependencias:
  ```bash
  cd frontend
  npm install
  ```
- Iniciar el servidor de desarrollo:
  ```bash
  npm run dev
  ```

## Estructura del Backend

```
backend/
├── app.py              # Punto de entrada Flask
├── auth.py             # Funciones de autenticación y autorización
├── cargar_todo.py      # Script para cargar todos los datos
├── requirements.txt    # Dependencias
├── data/               # Archivos CSV generados
├── uploads/            # Archivos DBF originales
├── models/             # Modelos de la base de datos
├── routes/             # Rutas de la API (auth, files, admin, metrics)
├── utils/              # Scripts de conversión y carga
└── migrations/         # Migraciones de la base de datos
```

### Principales rutas (blueprints):

- `/auth` - Registro y login
- `/files` - Carga y procesamiento de archivos DBF
- `/admin` - Acciones administrativas (cargar datos a la BD)
- `/api/metrics` - Métricas y estadísticas

## Estructura del Frontend

```
frontend/
├── src/
│   ├── App.jsx           # Componente principal y rutas
│   ├── Api.jsx           # Configuración de Axios
│   ├── context/
│   │   └── AuthContext.jsx # Contexto de autenticación
│   ├── components/
│   │   └── PrivateRoute.jsx # Protección de rutas
│   ├── pages/
│   │   ├── Dashboard.jsx   # Layout principal
│   │   ├── Login.jsx       # Página de login
│   │   ├── Upload.jsx      # Carga de archivos
│   │   └── Metrics.jsx     # Panel de métricas
│   └── index.css
├── public/
│   └── loguito.webp, logo-dipaolo.webp, etc.
└── ...
```

## Modelos de Datos

### Cliente

- `documento` (PK)
- `apellido`
- `telefono`
- `domicilio`
- `estado`
- Relación: muchos créditos

### Credito

- `num_credito` (PK)
- `documento` (FK a Cliente)
- `vendedor`, `sucursal`, `num_factura`, `fecha_real`, ...
- `total_facturado`, `anticipo`, `financiacion`, ...
- `num_cuotas`, `vto_primer_cuota`, ...
- Hasta 7 artículos y cantidades
- `garante`, `domicilio_garante`
- Relación: muchos pagos

### Pago

- `id` (PK)
- `num_credito` (FK a Credito)
- `num_cuota`, `vencimiento`, `fecha_pago`, `importe`, `importe_pago`, `vendedor`
- Restricción única: (num_credito, num_cuota)

### Usuario

- `id` (PK)
- `nombre`, `email` (único), `password_hash`, `rol` (usuario/admin)

## Rutas y Endpoints Principales

### Autenticación

- `POST /auth/register` - Registro de usuario
- `POST /auth/login` - Login, retorna JWT

### Archivos y Procesamiento

- `POST /files/upload` - (admin) Sube archivos DBF, los convierte a CSV
- `POST /admin/cargar_datos` - (admin) Carga los CSV a la base de datos

### Métricas y Datos

- `GET /api/metrics/creditos` - Métricas de créditos
- `GET /api/metrics/clientes` - Métricas de clientes

### Ejemplo de flujo de carga de datos:

1. Subir archivos DBF desde el frontend (Upload)
2. El backend los convierte automáticamente a CSV
3. Ejecutar carga a la base de datos (botón o petición a `/admin/cargar_datos`)
4. Visualizar métricas y datos en el panel

## Flujo de Procesamiento de Archivos

1. **Carga de archivos:** El usuario administrador sube `cremae.dbf` y `crepag.dbf` desde el frontend.
2. **Conversión:** El backend convierte los DBF a CSV (`creditos.csv`, `pagos.csv`, `clientes.csv`).
3. **Carga a la base:** El admin ejecuta la carga de los CSV a la base de datos.
4. **Visualización:** Los datos quedan disponibles para consulta y métricas.

## Autenticación y Autorización

- **JWT:** El login retorna un token JWT que debe enviarse en el header `Authorization: Bearer <token>`.
- **Roles:** Hay rutas exclusivas para administradores (carga de archivos y datos).
- **Protección en frontend:** Las rutas están protegidas con `PrivateRoute` y el contexto de autenticación.

## Notas de Seguridad y Buenas Prácticas

- Mantener segura la clave `SECRET_KEY` y las credenciales de la base de datos.
- Realizar respaldos periódicos de la base de datos.
- Verificar la integridad de los archivos DBF antes de procesarlos.
- Los archivos CSV generados se sobrescriben en cada conversión.
- No exponer el backend a internet sin HTTPS y sin restringir los orígenes permitidos en CORS.

## Ejemplos de Uso de la API

### 1. Registro de usuario

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Perez",
    "email": "juan@ejemplo.com",
    "password": "12345678"
  }'
```

**Respuesta exitosa:**

```json
{
  "mensaje": "Usuario registrado correctamente"
}
```

### 2. Login (obtener token JWT)

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@ejemplo.com",
    "password": "12345678"
  }'
```

**Respuesta exitosa:**

```json
{
  "token": "<JWT>"
}
```

### 3. Subir archivos DBF (admin)

```bash
curl -X POST http://localhost:5000/files/upload \
  -H "Authorization: Bearer <JWT>" \
  -F "cremae=@/ruta/cremae.dbf" \
  -F "crepag=@/ruta/crepag.dbf"
```

**Respuesta exitosa:**

```json
{
  "mensaje": "Archivos cargados y CSVs generados correctamente. Ejecutá /admin/cargar_datos para cargar en BD."
}
```

### 4. Cargar datos a la base de datos (admin)

```bash
curl -X POST http://localhost:5000/admin/cargar_datos \
  -H "Authorization: Bearer <JWT>"
```

**Respuesta exitosa:**

```json
{
  "mensaje": "Datos cargados correctamente"
}
```

### 5. Obtener métricas de créditos

```bash
curl -X GET http://localhost:5000/api/metrics/creditos \
  -H "Authorization: Bearer <JWT>"
```

**Respuesta exitosa (ejemplo):**

```json
{
  "creditos_activos": 120,
  "importe_total_creditos_activos": 500000,
  "importe_pagado_creditos_activos": 350000,
  "importe_atrasado_creditos_activos": 20000,
  "importe_deuda_creditos_activos": 130000,
  "porcentaje_pagado_creditos_activos": 70.0,
  "porcentaje_deuda_creditos_activos": 26.0,
  "porcentaje_atrasado_creditos_activos": 4.0,
  "cuotas_totales_creditos_activos": 800,
  "porcentaje_cuotas_pagadas_creditos_activos": 75.0,
  "porcentaje_cuotas_no_pagadas_creditos_activos": 25.0
}
```

### 6. Obtener métricas de clientes

```bash
curl -X GET http://localhost:5000/api/metrics/clientes \
  -H "Authorization: Bearer <JWT>"
```

**Respuesta exitosa (ejemplo):**

```json
{
  "al_dia": { "cantidad": 80, "porcentaje": 66.7 },
  "atrasados": { "cantidad": 30, "porcentaje": 25.0 },
  "morosos": { "cantidad": 10, "porcentaje": 8.3 }
}
```

---

## Créditos y Licencia

Desarrollado por el equipo de Pasantías Di Paolo. Uso interno. Para dudas o mejoras, contactar a los responsables del proyecto.
