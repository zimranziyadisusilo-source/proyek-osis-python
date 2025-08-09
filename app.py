# app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# --- DATABASE SEMENTARA (versi Python) ---
users = {
    "siswa01": {"password": "123", "telahMemilih": False},
    "siswa02": {"password": "456", "telahMemilih": False},
    "siswa03": {"password": "789", "telahMemilih": False},
    "admin": {"password": "admin", "telahMemilih": False}
}

vote_count = {
    "kandidat1": {"nama": "Zimran", "suara": 0},
    "kandidat2": {"nama": "Raden", "suara": 0},
    "kandidat3": {"nama": "Aldis", "suara": 0}
}
# ---------------------------------------------

@app.route('/')
def index():
    return render_template('1-login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = users.get(username)
    if user and user['password'] == password:
        if user['telahMemilih']:
            return redirect(url_for('hasil', user=username))
        else:
            return redirect(url_for('kandidat', user=username))
    else:
        return '<h1>Login Gagal!</h1><p>Username atau Password salah. <a href="/">Coba lagi</a></p>'

@app.route('/kandidat')
def kandidat():
    return render_template('2-kandidat.html')

@app.route('/voting')
def voting():
    username = request.args.get('user')
    user = users.get(username)
    if not user or user['telahMemilih']:
        return redirect(url_for('hasil', user=username))
    else:
        return render_template('3-voting.html', username=username)

@app.route('/vote', methods=['POST'])
def vote():
    username = request.form['username']
    kandidat = request.form['kandidat']
    user = users.get(username)
    if user and not user['telahMemilih']:
        user['telahMemilih'] = True
        if kandidat in vote_count:
            vote_count[kandidat]['suara'] += 1
        return redirect(url_for('hasil', user=username))
    else:
        return '<h1>Aksi tidak valid!</h1><a href="/">Login ulang</a></p>'

@app.route('/hasil')
def hasil():
    return render_template('4-hasil.html')

@app.route('/api/results')
def api_results():
    return jsonify(vote_count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)