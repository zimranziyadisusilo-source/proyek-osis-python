# app.py (versi dengan SQLite)

import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

DATABASE = 'database.db'

def get_db_connection():
    """Membuat koneksi ke database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Agar bisa mengakses kolom dengan nama
    return conn

# Route untuk halaman utama (login)
@app.route('/')
def index():
    return render_template('1-login.html')

# Route untuk proses login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    # Mencari user di database
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user and user['password'] == password:
        if user['telahMemilih'] == 1:
            return redirect(url_for('hasil', user=username))
        else:
            return redirect(url_for('kandidat', user=username))
    else:
        return '<h1>Login Gagal!</h1><p>Username atau Password salah. <a href="/">Coba lagi</a></p>'

# Route untuk halaman kandidat
@app.route('/kandidat')
def kandidat():
    return render_template('2-kandidat.html')

# Route untuk halaman voting
@app.route('/voting')
def voting():
    username = request.args.get('user')
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    kandidat_list = conn.execute('SELECT * FROM kandidat').fetchall()
    conn.close()

    if not user or user['telahMemilih'] == 1:
        return redirect(url_for('hasil', user=username))
    else:
        # Mengirim data kandidat ke template
        return render_template('3-voting.html', username=username, kandidat_list=kandidat_list)


# Route untuk memproses suara
@app.route('/vote', methods=['POST'])
def vote():
    username = request.form['username']
    kandidat_id = request.form['kandidat']

    conn = get_db_connection()
    try:
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        # Pengecekan utama: apakah user ada dan belum memilih?
        if user and user['telahMemilih'] == 0:
            # Memulai transaksi
            conn.execute('BEGIN')
            # Aksi 1: Update status pemilih
            conn.execute('UPDATE users SET telahMemilih = 1 WHERE username = ?', (username,))
            # Aksi 2: Tambah suara kandidat
            conn.execute('UPDATE kandidat SET suara = suara + 1 WHERE id = ?', (kandidat_id,))
            # Jika kedua aksi berhasil, simpan permanen
            conn.commit()
            return redirect(url_for('hasil', user=username))
        else:
            # Jika user tidak valid atau sudah memilih
            return '<h1>Aksi tidak valid!</h1><p>Anda mungkin sudah memilih atau sesi Anda tidak valid. <a href="/">Login ulang</a></p>'
    except sqlite3.Error as e:
        # Jika terjadi error database di tengah jalan, batalkan semua perubahan
        conn.rollback()
        print(f"Database error: {e}") # Untuk debugging di server log
        return "<h1>Terjadi kesalahan pada server. Silakan coba lagi.</h1>"
    finally:
        # Apapun yang terjadi, pastikan koneksi database ditutup
        if conn:
            conn.close()
# Route untuk halaman hasil
@app.route('/hasil')
def hasil():
    return render_template('4-hasil.html')

# Route API untuk memberikan data hasil (untuk live count)
@app.route('/api/results')
def api_results():
    conn = get_db_connection()
    kandidat_rows = conn.execute('SELECT * FROM kandidat ORDER BY id').fetchall()
    conn.close()
    
    # Mengubah data dari database menjadi format dictionary yang sama seperti sebelumnya
    vote_count = {row['id']: {"nama": row['nama'], "suara": row['suara']} for row in kandidat_rows}
    return jsonify(vote_count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)