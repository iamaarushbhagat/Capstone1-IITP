from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3, random

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DB = 'ev_data.db'

def get_db(): 
    return sqlite3.connect(DB)

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM admins WHERE username=? AND password=?", (u, p))
        if c.fetchone():
            session["user"] = u
            return redirect("/vehicles")
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/vehicles")
def vehicles():
    if "user" not in session:
        return redirect("/login")
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM vehicles")
    vehs = c.fetchall()
    return render_template("vehicles.html", vehicles=vehs)

@app.route("/dashboard/<int:vid>")
def dashboard(vid):
    if "user" not in session:
        return redirect("/login")
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM vehicles WHERE id=?", (vid,))
    row = c.fetchone()
    if not row:
        return "Not found", 404
    vehicle = {"id": row[0], "brand": row[1], "plate": row[2], "name": row[3]}
    return render_template("dashboard.html", vehicle=vehicle)

@app.route("/api/vehicle/<int:vid>")
def api_vehicle(vid):
    soc = round(random.uniform(30, 100), 1)
    volt = round(random.uniform(360, 420), 2)
    bt = round(random.uniform(25, 60), 1)
    rpm = random.randint(2000, 7000)
    torque = round(random.uniform(50, 200), 2)
    mt = round(random.uniform(30, 90), 1)
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO vehicle_logs(vehicle_id, soc, voltage, bat_temp, rpm, torque, motor_temp) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (vid, soc, volt, bt, rpm, torque, mt)
    )
    conn.commit()
    return {
        "battery": {"SOC": soc, "Voltage": volt, "Temperature": bt},
        "motor": {"RPM": rpm, "Torque": torque, "Temperature": mt}
    }

@app.route("/api/history/<int:vid>")
def history(vid):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT timestamp, soc, rpm, bat_temp, motor_temp FROM vehicle_logs WHERE vehicle_id=? ORDER BY id DESC LIMIT 20",
        (vid,)
    )
    rows = c.fetchall()
    data = [
        {"time": r[0][-8:], "soc": r[1], "rpm": r[2], "bat_temp": r[3], "motor_temp": r[4]}
        for r in reversed(rows)
    ]
    return jsonify(data)

@app.route("/admin_panel")
def admin_panel():
    if "user" not in session:
        return redirect("/login")
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM vehicles")
    vehs = c.fetchall()
    return render_template("admin_panel.html", vehicles=vehs)

@app.route("/admin/add", methods=["POST"])
def admin_add():
    if "user" not in session:
        return redirect("/login")
    brand = request.form["brand"]
    plate = request.form["plate"]
    name = request.form["name"]
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO vehicles (brand, plate, name) VALUES (?, ?, ?)",
        (brand, plate, name)
    )
    conn.commit()
    return redirect("/admin_panel")

@app.route("/admin/edit/<int:vid>", methods=["POST"])
def admin_edit(vid):
    if "user" not in session:
        return redirect("/login")
    brand = request.form["brand"]
    plate = request.form["plate"]
    name = request.form["name"]
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "UPDATE vehicles SET brand=?, plate=?, name=? WHERE id=?",
        (brand, plate, name, vid)
    )
    conn.commit()
    return redirect("/admin_panel")

@app.route("/admin/delete/<int:vid>")
def admin_delete(vid):
    if "user" not in session:
        return redirect("/login")
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM vehicles WHERE id=?", (vid,))
    conn.commit()
    return redirect("/admin_panel")

if __name__ == "__main__":
    app.run(debug=True)
