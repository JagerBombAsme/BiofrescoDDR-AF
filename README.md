1. Requisitos Previos

Antes de ejecutar el sistema, debe cumplirse lo siguiente.

1.1. Python 3.10 o Superior

Debe descargarse e instalarse Python desde:

https://www.python.org/downloads/

Durante la instalación, debe habilitarse la opción:

Add Python to PATH

1.2. Visual Studio Code

Debe utilizarse Visual Studio Code para la gestión del proyecto.

Descarga:

https://code.visualstudio.com/

Debe instalarse la extensión:

Python (Microsoft)

1.3. Git (Opcional)

Si el proyecto se obtiene desde GitHub, Git debe estar instalado.

Descarga:

https://git-scm.com/downloads

2. Instalación y Ejecución del Sistema

Los pasos descritos a continuación deben ejecutarse en el orden indicado.

2.1. Apertura del Proyecto

La carpeta del proyecto debe ubicarse en una ruta accesible.

Visual Studio Code debe abrirse.

La carpeta principal del sistema debe seleccionarse mediante:
File → Open Folder.

2.2. Creación del Entorno Virtual

Debe abrirse una terminal y ejecutar:

python -m venv venv


El entorno virtual debe activarse según el sistema operativo:

Sistema	Comando
Windows	venv\Scripts\activate
Linux/Mac	source venv/bin/activate

La terminal debe mostrar el prefijo (venv).

2.3. Instalación de Dependencias

Debe ejecutarse:

pip install -r requirements.txt


Si no existe archivo requirements.txt, deben instalarse las librerías esenciales:

pip install django
pip install openpyxl
pip install pillow

2.4. Migraciones de Base de Datos

Para crear las tablas del sistema, debe ejecutarse:

python manage.py migrate

2.5. Creación del Superusuario

Debe crearse un superusuario mediante:

python manage.py createsuperuser

2.6. Ejecución del Servidor

Debe iniciarse el servidor con:

python manage.py runserver


El sistema debe quedar disponible en:

http://127.0.0.1:8000/

3. Uso del Sistema
3.1. Acceso al Panel Administrativo

Debe accederse a:

http://127.0.0.1:8000/admin

3.2. Módulo de Productos

Ruta: Inventario → Productos

En este módulo deben gestionarse:

creación de productos

edición de productos

eliminación (solo si no poseen movimientos registrados)

Estados automáticos del inventario:

Estado	Condición
Agotado	Stock = 0
Crítico	Stock < stock mínimo
Bajo	Stock entre mínimo y 1.5 × mínimo
Normal	Stock > 1.5 × mínimo
3.3. Módulo de Movimientos

Ruta: Movimientos

Deben registrarse operaciones de:

Entrada

Salida

Merma

Ajuste

Las Entradas deben asociarse obligatoriamente a un proveedor.

3.4. Módulo de Proveedores

Ruta: Proveedores

Deben administrarse proveedores activos e inactivos.
Las Entradas requieren un proveedor válido.

3.5. Módulo de Transportistas

Ruta: Transportistas

Debe mantenerse información de transportistas, empresas, teléfonos y patentes.

3.6. Inventario General

Ruta: Inventario general

Debe utilizarse para visualizar el estado completo del inventario, filtrar por estado o buscar productos.

3.7. Reportes

Ruta: Reportes

Deben generarse archivos Excel correspondientes a:

Movimientos

Inventario general

Proveedores

4. Gestión Avanzada y Solución de Problemas
4.1. Archivos Estáticos

Las imágenes deben almacenarse en:

/static/img/


Para utilizarlas en plantillas Django, debe emplearse:

{% static "img/nombre_de_la_imagen.png" %}

4.2. Errores Frecuentes
Mensaje	Causa	Acción Correctiva
pip no se reconoce	Python no fue agregado al PATH	Reinstalar Python habilitando Add Python to PATH
ModuleNotFoundError	Dependencias faltantes	Ejecutar pip install -r requirements.txt
Permission denied	Permisos insuficientes	Ejecutar VS Code con permisos elevados
4.3. Detención del Servidor

Debe detenerse con:

CTRL + C

4.4. Salida del Entorno Virtual

Debe ejecutarse:

deactivate
