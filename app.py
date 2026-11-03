import sqlite3
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.secret_key = "cambia-esta-clave"
DB = "minimarket.db"
STOCK_MINIMO = 5


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_):
    db = g.pop("db", None)
    if db:
        db.close()


def init_db():
    db = sqlite3.connect(DB)
    db.executescript("""
    CREATE TABLE IF NOT EXISTS productos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS ventas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        total REAL NOT NULL);
    CREATE TABLE IF NOT EXISTS detalle_venta(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venta_id INTEGER NOT NULL REFERENCES ventas(id),
        producto_id INTEGER NOT NULL REFERENCES productos(id),
        cantidad INTEGER NOT NULL,
        subtotal REAL NOT NULL);
    """)
    db.commit()
    db.close()


# RF1: Registrar producto / RF2: Listar, editar y eliminar productos
@app.route("/")
@app.route("/productos")
def productos():
    lista = get_db().execute("SELECT * FROM productos ORDER BY nombre").fetchall()
    return render_template("productos.html", productos=lista, minimo=STOCK_MINIMO)


@app.route("/productos/nuevo", methods=["POST"])
def producto_nuevo():
    nombre = request.form["nombre"].strip()
    try:
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])
        assert nombre and precio >= 0 and stock >= 0
    except (ValueError, AssertionError):
        flash("Datos inválidos. Revisa nombre, precio y stock.", "error")
        return redirect(url_for("productos"))
    db = get_db()
    db.execute("INSERT INTO productos(nombre,precio,stock) VALUES(?,?,?)", (nombre, precio, stock))
    db.commit()
    flash(f"Producto «{nombre}» registrado.", "ok")
    return redirect(url_for("productos"))


@app.route("/productos/<int:pid>/editar", methods=["GET", "POST"])
def producto_editar(pid):
    db = get_db()
    p = db.execute("SELECT * FROM productos WHERE id=?", (pid,)).fetchone()
    if not p:
        return redirect(url_for("productos"))
    if request.method == "POST":
        db.execute("UPDATE productos SET nombre=?, precio=?, stock=? WHERE id=?",
                   (request.form["nombre"].strip(), float(request.form["precio"]),
                    int(request.form["stock"]), pid))
        db.commit()
        flash("Producto actualizado.", "ok")
        return redirect(url_for("productos"))
    return render_template("editar.html", p=p)


@app.route("/productos/<int:pid>/eliminar", methods=["POST"])
def producto_eliminar(pid):
    db = get_db()
    try:
        db.execute("DELETE FROM productos WHERE id=?", (pid,))
        db.commit()
        flash("Producto eliminado.", "ok")
    except sqlite3.IntegrityError:
        flash("No se puede eliminar: tiene ventas asociadas.", "error")
    return redirect(url_for("productos"))


# RF3: Registrar venta / RF4: Descontar inventario automáticamente
@app.route("/venta", methods=["GET", "POST"])
def venta():
    db = get_db()
    disponibles = db.execute("SELECT * FROM productos WHERE stock>0 ORDER BY nombre").fetchall()
    if request.method == "POST":
        items, total = [], 0
        for p in disponibles:
            cant = request.form.get(f"cant_{p['id']}", "0")
            cant = int(cant) if cant.isdigit() else 0
            if cant <= 0:
                continue
            if cant > p["stock"]:
                flash(f"Stock insuficiente de «{p['nombre']}» (quedan {p['stock']}).", "error")
                return redirect(url_for("venta"))
            sub = cant * p["precio"]
            items.append((p["id"], cant, sub))
            total += sub
        if not items:
            flash("Selecciona al menos un producto.", "error")
            return redirect(url_for("venta"))
        cur = db.execute("INSERT INTO ventas(fecha,total) VALUES(?,?)", (date.today().isoformat(), total))
        for pid, cant, sub in items:
            db.execute("INSERT INTO detalle_venta(venta_id,producto_id,cantidad,subtotal) VALUES(?,?,?,?)",
                       (cur.lastrowid, pid, cant, sub))
            db.execute("UPDATE productos SET stock = stock - ? WHERE id=?", (cant, pid))
        db.commit()
        flash(f"Venta registrada. Total: ${total:,.0f}", "ok")
        return redirect(url_for("venta"))
    return render_template("venta.html", productos=disponibles)


# RF5: Alerta de stock bajo
@app.route("/alertas")
def alertas():
    bajos = get_db().execute("SELECT * FROM productos WHERE stock<=? ORDER BY stock",
                             (STOCK_MINIMO,)).fetchall()
    return render_template("alertas.html", productos=bajos, minimo=STOCK_MINIMO)


# RF6: Reporte de ventas por día
@app.route("/reporte")
def reporte():
    dia = request.args.get("fecha", date.today().isoformat())
    db = get_db()
    ventas = db.execute("SELECT * FROM ventas WHERE fecha=? ORDER BY id DESC", (dia,)).fetchall()
    detalle = db.execute("""SELECT p.nombre, SUM(d.cantidad) AS unidades, SUM(d.subtotal) AS total
        FROM detalle_venta d JOIN ventas v ON v.id=d.venta_id
        JOIN productos p ON p.id=d.producto_id WHERE v.fecha=?
        GROUP BY p.id ORDER BY unidades DESC""", (dia,)).fetchall()
    total_dia = sum(v["total"] for v in ventas)
    return render_template("reporte.html", dia=dia, ventas=ventas, detalle=detalle, total_dia=total_dia)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
