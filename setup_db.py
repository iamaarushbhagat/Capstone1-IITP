import sqlite3, os

DB = 'ev_data.db'
if os.path.exists(DB):
    os.remove(DB)

conn = sqlite3.connect(DB)
c = conn.cursor()

c.execute('''
CREATE TABLE vehicles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  brand TEXT NOT NULL,
  plate TEXT NOT NULL,
  name TEXT NOT NULL
)
''')
vehicles = [
  ('Tata','MH12AB1234','Nexon EV'),
  ('Mahindra','DL05XY4321','XUV400'),
  ('Maruti','KA03MP7654','WagonR EV'),
  ('Hyundai','TN22GH9988','Kona EV'),
  ('MG','GJ18TR6572','ZS EV')
]
c.executemany('INSERT INTO vehicles (brand,plate,name) VALUES (?,?,?)', vehicles)

c.execute('''
CREATE TABLE admins (
  username TEXT PRIMARY KEY,
  password TEXT NOT NULL
)
''')
c.execute("INSERT INTO admins VALUES ('admin','admin123')")

c.execute('''
CREATE TABLE vehicle_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  vehicle_id INTEGER,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  soc REAL, voltage REAL, bat_temp REAL,
  rpm INTEGER, torque REAL, motor_temp REAL
)
''')

conn.commit()
conn.close()
print("✅ Database initialized.")

