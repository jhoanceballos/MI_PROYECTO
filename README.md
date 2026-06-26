# 🛡️ SafeZone - Plataforma Web de Seguridad y Gestión

SafeZone es una aplicación web robusta construida con **Django** y **MySQL**, completamente dockerizada, diseñada para la gestión segura de usuarios, control de accesos por roles y administración centralizada.

---

## 🏗️ Arquitectura del Sistema y Capas

El proyecto sigue una arquitectura monolítica limpia basada en el patrón de diseño propio de Django: **MVT (Modelo-Vista-Template)**, acoplada a un aislamiento por contenedores con Docker.

### 📐 Capas Principales:
1. **Capa de Presentación (Templates):** Construida con HTML5, CSS3 y **Bootstrap** para garantizar una interfaz responsiva, limpia y amigable con el usuario.
2. **Capa de Lógica de Negocio (Views):** Controladores en Python que gestionan las peticiones HTTP (`GET`/`POST`), procesan formularios y aplican validaciones estrictas.
3. **Capa de Datos (Models):** Capa de abstracción de base de datos (ORM de Django) conectada de manera persistente a un contenedor dedicado de **MySQL**.

---

## 🎨 Patrones de Diseño Aplicados

### 1. Object-Relational Mapping (ORM)
Se utiliza el ORM nativo de Django para interactuar con MySQL sin escribir consultas SQL crudas. Esto previene ataques comunes y abstrae la base de datos en clases de Python (`Usuario`, `Rol`).

### 2. Singleton (Estructura de Configuración)
El archivo `settings.py` actúa bajo el concepto de Singleton, sirviendo como un único punto de verdad global para las variables de entorno, configuraciones de bases de datos y middleware de la aplicación.

### 3. Decorator (Decoradores de Python)
Utilizado de manera extensiva para interceptar peticiones y añadir comportamiento a las funciones de las vistas sin modificar su código interno (ej. `@login_required` y `@admin_required`).

---

## 🔒 Capas de Seguridad Implementadas

La seguridad es el pilar fundamental de **SafeZone**. Se implementaron controles estrictos en múltiples niveles del framework:

* **Autenticación y Autorización Basada en Roles (RBAC):** Sistema personalizado donde los usuarios tienen asignado un modelo `Rol` (`Administrador`, `Usuario Común`). Los accesos a paneles críticos están protegidos mediante decoradores personalizados.
* **Protección contra Cross-Site Request Forgery (CSRF):** Uso obligatorio del token `{% csrf_token %}` en todos los formularios (`POST`) de la aplicación para evitar la suplantación de identidad en las peticiones.
* **Manejo Seguro de Archivos Multimedia (Media Security):** Restricción estricta de permisos de escritura y lectura física (`chmod 777` controlado por usuario administrador) en las carpetas destinadas a almacenar imágenes de perfil, previniendo la inyección de scripts ejecutables en el servidor.
* **Protección contra Inyección SQL:** Al utilizar el ORM de Django, todos los parámetros de búsqueda y guardado son sanitizados automáticamente mediante consultas preparadas.
* **Protección de Credenciales (Hashing):** Las contraseñas de los usuarios nunca se guardan en texto plano en MySQL; son encriptadas usando el algoritmo de hashing seguro **PBKDF2 con SHA256**.
* **Aislamiento por Variables de Entorno:** Uso de `os.environ.get()` en `settings.py` para asegurar que las credenciales de producción de MySQL (`DB_PASSWORD`, `DB_HOST`) no queden expuestas en el código fuente.

---

## 🚀 Requisitos e Instalación con Docker

### Requisitos Previos:
* Docker y Docker Compose instalados en tu sistema operativo (Linux/Windows).

### Pasos para Ejecutar el Proyecto:

1. Clonar el repositorio en tu máquina local.
2. Construir y encender los contenedores (Django + MySQL) en segundo plano o con logs activos:
   ```bash
   sudo docker compose up --build