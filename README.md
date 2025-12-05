README – Guía de Instalación y Uso del Sistema de Inventario (Django)

Este documento explica, paso a paso, cómo instalar, ejecutar y administrar el sistema de inventario desarrollado en Django. Está escrito en un lenguaje claro y directo, orientado a usuarios con conocimientos técnicos básicos.

1. Requisitos Previos

Antes de comenzar, se deben instalar las siguientes herramientas.

1.1. Python 3.10 o Superior

Lenguaje en el que está desarrollado el sistema.

Descarga: https://www.python.org/downloads/

Durante la instalación, es indispensable marcar la opción:

[x] Add Python to PATH

1.2. Visual Studio Code

Editor de código recomendado para abrir y ejecutar el proyecto.

Descarga: https://code.visualstudio.com/

Extensión necesaria:

Python (Microsoft)


2. Instalación y Ejecución del Sistema

Siga los siguientes pasos en orden.

2.1. Abrir el Proyecto en Visual Studio Code

Coloque la carpeta del proyecto en una ruta fácil de recordar.

Abra Visual Studio Code.

Menú: File → Open Folder

Seleccione la carpeta principal del proyecto.

2.2. Crear el Entorno Virtual

Un entorno virtual (venv) permite aislar las librerías del proyecto.

Abra la terminal en VS Code:

Terminal → New Terminal


Crear el entorno:

python -m venv venv


Activar el entorno según sistema operativo:

Sistema Operativo	Comando
Windows	venv\Scripts\activate
Linux / Mac	source venv/bin/activate

Si funciona correctamente, la terminal mostrará:

(venv) C:\ruta\del\proyecto>

2.3. Instalar Dependencias

Ejecutar:

pip install -r requirements.txt


Si no posee archivo requirements.txt, instalar manualmente:

pip install django
pip install openpyxl
pip install pillow

2.4. Migrar la Base de Datos

Crear las tablas necesarias:

python manage.py makemigrations
python manage.py migrate

2.5. Crear el Usuario Administrador

Ejecutar:

python manage.py createsuperuser


Ingresar nombre de usuario, correo (opcional) y contraseña.

2.6. Ejecutar el Servidor

Iniciar el sistema:

python manage.py runserver


Acceder desde el navegador:

http://127.0.0.1:8000/

3. Uso del Sistema – Módulos Principales
3.1. Acceso al Panel Administrativo

Ir a:

http://127.0.0.1:8000/admin


Iniciar sesión con el superusuario creado.

3.2. Productos

Ruta: Inventario → Productos

Permite administrar el catálogo de productos.

Acciones disponibles:

Crear productos

Editar productos

Eliminar productos (si no tienen movimientos registrados)

Campos del formulario:

Código

Nombre

Unidad base (Kg, Unidades, Litros)

Stock mínimo

Descripción (opcional)

Estados automáticos del producto:

Estado	Descripción
Agotado	Stock igual a 0
Crítico	Stock menor al mínimo
Bajo	Stock entre el mínimo y 1.5 × mínimo
Normal	Stock mayor que 1.5 × mínimo
3.3. Movimientos

Ruta: Movimientos

Permite actualizar el inventario mediante registros de movimiento.

Tipos de movimiento:

Entrada (incrementa stock; requiere proveedor)

Salida (reduce stock)

Merma (reduce stock por pérdida)

Ajuste (corrección manual)

3.4. Proveedores

Ruta: Proveedores

Permite agregar, editar e inactivar proveedores.
Obligatorios para registrar Entradas.

3.5. Transportistas

Ruta: Transportistas
Permite registrar información de logística, choferes y empresas asociadas.

3.6. Inventario General

Ruta: Inventario general

Muestra:

Stock actual

Estados del inventario

Filtros por estado

Búsqueda por nombre o código

3.7. Reportes

Ruta: Reportes

Exportación a Excel de:

Movimientos

Inventario general

Proveedores

4. Gestión Avanzada y Solución de Problemas
4.1. Archivos Estáticos (Imágenes y CSS)

Las imágenes deben ubicarse en:

/static/img/


Para utilizarlas en plantillas Django:

{% static "img/nombre_de_la_imagen.png" %}

4.2. Errores Comunes
Mensaje	Causa	Solución
pip no se reconoce	Python no se agregó al PATH	Reinstalar Python y marcar “Add Python to PATH”
ModuleNotFoundError	Faltan librerías	Ejecutar pip install -r requirements.txt
Permission denied	Permisos insuficientes	Ejecutar VS Code como administrador
4.3. Detener el Servidor

Presionar:

CTRL + C

4.4. Salir del Entorno Virtual

Ejecutar:

deactivate
