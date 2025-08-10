# database_setup.py
import sqlite3

# Menghubungkan ke database (akan membuat file database.db jika belum ada)
conn = sqlite3.connect('database.db')
print("Database berhasil dibuat atau dihubungkan.")

# Membuat cursor untuk mengeksekusi perintah SQL
cursor = conn.cursor()

# Membuat tabel 'users'
# id: Nomor unik untuk setiap user
# username: Nama user (harus unik)
# password: Password user
# telahMemilih: Status memilih (0 untuk belum, 1 untuk sudah)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    telahMemilih INTEGER NOT NULL
);
''')
print("Tabel 'users' berhasil dibuat.")

# Membuat tabel 'kandidat'
# id: Nomor unik untuk setiap kandidat (kandidat1, kandidat2, dst)
# nama: Nama pasangan calon
# suara: Jumlah suara yang didapat
cursor.execute('''
CREATE TABLE IF NOT EXISTS kandidat (
    id TEXT PRIMARY KEY,
    nama TEXT NOT NULL,
    suara INTEGER NOT NULL
);
''')
print("Tabel 'kandidat' berhasil dibuat.")

# Mengisi data awal ke tabel 'users'
initial_users = [
    ("siswa01", "123", 0),
    ("siswa02", "456", 0),
    ("siswa03", "789", 0),
    ("admin", "admin", 1) # Admin dianggap sudah memilih
]
cursor.executemany('INSERT OR IGNORE INTO users (username, password, telahMemilih) VALUES (?, ?, ?)', initial_users)
print("Data awal user berhasil dimasukkan.")


# Mengisi data awal ke tabel 'kandidat'
initial_kandidat = [
    ("kandidat1", "Zimran", 0),
    ("kandidat2", "Raden", 0),
    ("kandidat3", "Aldis", 0)
]
cursor.executemany('INSERT OR IGNORE INTO kandidat (id, nama, suara) VALUES (?, ?, ?)', initial_kandidat)
print("Data awal kandidat berhasil dimasukkan.")

# Menyimpan perubahan (commit) dan menutup koneksi
conn.commit()
conn.close()
print("Perubahan telah disimpan dan koneksi ditutup.")