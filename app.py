from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('ev_diagnostics.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/vehicles')
def get_vehicles():
    conn = get_db_connection()
    vehicles = conn.execute('SELECT * FROM Vehicle').fetchall()
    conn.close()
    return jsonify([dict(v) for v in vehicles])

@app.route('/api/logs')
def get_logs():
    conn = get_db_connection()
    logs = conn.execute('SELECT * FROM Diagnostics_Log ORDER BY timestamp DESC').fetchall()
    conn.close()
    return jsonify([dict(l) for l in logs])

@app.route('/api/add_log', methods=['POST'])
def add_log():
    data = request.json
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO Diagnostics_Log (vehicle_id, error_code, message, sensor_type, sensor_value, unit) VALUES (?, ?, ?, ?, ?, ?)',
        (data['vehicle_id'], data['error_code'], data['message'], data['sensor_type'], data['sensor_value'], data['unit'])
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
