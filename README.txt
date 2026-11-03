<div align="center">

# 🛒 Minimarket

**Sistema de gestión de productos y ventas para un minimarket**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![Licencia](https://img.shields.io/badge/software-libre-1f5f4a)

Prototipo funcional (MVP) · Ingeniería de Software · Metodología ágil

</div>

---

## 📋 Requisitos funcionales implementados

| Código | Requisito | Ruta |
|:------:|-----------|------|
| **RF1** | Registrar producto | `/productos` |
| **RF2** | Listar, editar y eliminar productos | `/productos` |
| **RF3** | Registrar venta con varios productos | `/venta` |
| **RF4** | Descontar inventario automáticamente al vender | `/venta` |
| **RF5** | Alerta de stock bajo (5 unidades o menos) | `/alertas` |
| **RF6** | Reporte de ventas por día | `/reporte` |

---

## 🧰 Tecnologías

| Capa | Herramienta |
|------|-------------|
| Backend | Python + Flask |
| Base de datos | SQLite |
| Frontend | HTML + CSS (plantillas Jinja2) |
| Editor | Visual Studio Code |

---

## 📁 Estructura del proyecto

```
minimarket/
├── app.py               # Lógica y rutas
├── requirements.txt     # Dependencias
├── README.md
├── static/
│   └── style.css        # Estilos
└── templates/
    ├── base.html        # Plantilla base (menú)
    ├── productos.html   # RF1 y RF2
    ├── editar.html      # RF2
    ├── venta.html       # RF3 y RF4
    ├── alertas.html     # RF5
    └── reporte.html     # RF6
```

> `minimarket.db` se crea automáticamente la primera vez que se ejecuta la app.

---

## 🚀 Instalación y ejecución

**1.** Instala [Python 3.10+](https://www.python.org) y marca **"Add Python to PATH"**.

**2.** Abre una terminal en la carpeta del proyecto:

```bash
cd C:\Users\TU_USUARIO\Downloads\minimarket
```

**3.** Crea el entorno virtual:

```bash
python -m venv venv
```

**4.** Actívalo *(si da error en PowerShell, ve a [Problema 1](#-problema-1-powershell-no-deja-activar-el-entorno-virtual))*:

```bash
venv\Scripts\activate
```

Si funciona, verás `(venv)` al inicio de la línea.

**5.** Instala las dependencias:

```bash
pip install -r requirements.txt
```

**6.** Ejecuta la aplicación:

```bash
python app.py
```

**7.** Abre en el navegador 👉 **http://127.0.0.1:5000**

**8.** Para detener el servidor: `Ctrl + C` en la terminal.

---

## 🛠️ Problemas encontrados y soluciones

### ⚠️ Problema 1: PowerShell no deja activar el entorno virtual

```
No se puede cargar el archivo ...\venv\Scripts\Activate.ps1 porque la
ejecución de scripts está deshabilitada en este sistema.
```

**Causa:** Windows bloquea por defecto los scripts de PowerShell.

**Soluciones (elige una):**

| Opción | Cómo |
|--------|------|
| ✅ Habilitar solo en esta ventana | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` y luego `venv\Scripts\activate` |
| 🔧 No activar el entorno | `venv\Scripts\python -m pip install -r requirements.txt` y `venv\Scripts\python app.py` |
| 💻 Usar CMD | Abrir **cmd** y ejecutar `venv\Scripts\activate.bat` |

---

### ⚠️ Problema 2: VS Code no muestra `minimarket.db`

> *"The file is not displayed in the text editor because it is either binary or uses an unsupported text encoding."*

**Causa:** `minimarket.db` es una base de datos SQLite (archivo binario). Es normal e indica que la app ya creó la base de datos.

**Qué hacer:**
- ❌ No pulses **Open Anyway**: puede dañar el archivo si se guarda.
- ✅ Para ver las tablas (`productos`, `ventas`, `detalle_venta`) usa la extensión **SQLite Viewer** o **SQLite** en VS Code, o el programa gratuito **DB Browser for SQLite**.
- Para usar el sistema solo necesitas el navegador; el `.db` no se edita a mano.

---

### ⚠️ Problema 3: Agrego un producto y no lo veo en VS Code

**Causa:** agregar productos desde la página solo modifica `minimarket.db`, no el código. Además, los visores SQLite muestran una "foto" del momento en que abriste el archivo.

**Solución:** cierra y reabre la pestaña del `.db`, o pulsa el botón de refrescar de la extensión (en DB Browser: `F5`). Verifica también que abres el `.db` de la misma carpeta desde donde ejecutas `python app.py`.

---

## 💾 Persistencia de datos

Los productos y ventas **no se borran** al cerrar la app: quedan guardados en `minimarket.db`.

Se perderían solo si:
- Borras `minimarket.db`
- Mueves o borras la carpeta sin llevarte ese archivo
- Descomprimes el `.zip` de nuevo en otra carpeta (empieza con una base vacía)

💡 **Consejo:** haz una copia de `minimarket.db` con los datos cargados antes de la sustentación.

**Reiniciar desde cero:** detén la app, borra `minimarket.db` y vuelve a ejecutar `python app.py`.

---

## 📝 Notas

- Cambia `app.secret_key` en `app.py` si el sistema se usa fuera de un entorno de pruebas.
- El stock mínimo para la alerta se configura con la constante `STOCK_MINIMO` en `app.py`.