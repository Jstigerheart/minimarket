# Minimarket - Prototipo de gestión
 
Sistema de gestión para un minimarket. Python (Flask) + SQLite + HTML/CSS. Todo software libre.
 
## Requisitos funcionales implementados
 
- RF1: Registrar producto
- RF2: Listar, editar y eliminar productos
- RF3: Registrar venta con varios productos
- RF4: Descontar inventario automáticamente al vender
- RF5: Alerta de stock bajo (5 unidades o menos)
- RF6: Reporte de ventas por día
## Estructura
 
```
minimarket/
  app.py              (lógica y rutas)
  requirements.txt
  static/style.css
  templates/          (base, productos, editar, venta, alertas, reporte)
```
 
La base de datos `minimarket.db` se crea sola la primera vez que se ejecuta la app.
 
## Instalación y ejecución (paso a paso)
 
1. Instalar Python 3.10 o superior (https://www.python.org). Marcar "Add Python to PATH".
2. Abrir una terminal en la carpeta del proyecto:
```
   cd C:\Users\TU_USUARIO\Downloads\minimarket
```
3. Crear el entorno virtual:
```
   python -m venv venv
```
4. Activar el entorno virtual (ver "Problema 1" si da error en PowerShell):
```
   venv\Scripts\activate
```
   Si funciona, aparece `(venv)` al inicio de la línea.
5. Instalar dependencias:
```
   pip install -r requirements.txt
```
6. Ejecutar la aplicación:
```
   python app.py
```
7. Abrir en el navegador: http://127.0.0.1:5000
8. Para detener el servidor: `Ctrl + C` en la terminal.
## Problemas encontrados y soluciones
 
### Problema 1: PowerShell no deja activar el entorno virtual
 
Error:
```
No se puede cargar el archivo ...\venv\Scripts\Activate.ps1 porque la ejecución
de scripts está deshabilitada en este sistema.
```
 
Causa: Windows bloquea por defecto los scripts de PowerShell.
 
Soluciones (cualquiera de las tres):
 
- Habilitar scripts solo para la ventana actual:
```
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  venv\Scripts\activate
```
- No activar el entorno y usar directamente el Python del venv:
```
  venv\Scripts\python -m pip install -r requirements.txt
  venv\Scripts\python app.py
```
- Usar CMD en lugar de PowerShell y ejecutar `venv\Scripts\activate.bat`.
### Problema 2: VS Code no muestra el archivo minimarket.db
 
Mensaje: "The file is not displayed in the text editor because it is either binary or uses an unsupported text encoding."
 
Causa: `minimarket.db` es una base de datos SQLite (archivo binario), no texto. Es normal e indica que la app ya creó la base de datos.
 
Qué hacer:
 
- No pulsar "Open Anyway" (puede dañar el archivo si se guarda).
- Para ver las tablas (`productos`, `ventas`, `detalle_venta`), usar la extensión **SQLite Viewer** o **SQLite** en VS Code, o el programa gratuito **DB Browser for SQLite**.
- Para usar el sistema no hace falta abrir el `.db`; solo el navegador.
## Notas
 
- Para reiniciar los datos desde cero: detener la app y borrar `minimarket.db`. Se creará vacío al volver a ejecutar.
- Cambiar `app.secret_key` en `app.py` si el sistema se usa fuera de un entorno de pruebas.