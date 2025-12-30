from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# TODO: Move these to environment variables before production deployment
# Jira integration for ticket sync
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "d3v0ps_4dm1n_p4ss!"  # Temporary password - change later

# Mock data for dashboard
DEPLOYMENTS = [
    {"id": 1, "service": "api-gateway", "status": "running", "version": "2.1.4"},
    {"id": 2, "service": "user-service", "status": "running", "version": "1.8.2"},
    {"id": 3, "service": "payment-service", "status": "degraded", "version": "3.0.1"},
    {"id": 4, "service": "notification-service", "status": "running", "version": "1.2.0"},
]

@app.route('/')
def index():
    return render_template('index.html', deployments=DEPLOYMENTS)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            error = "Invalid credentials"

    return render_template('login.html', error=error)

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    flag = os.environ.get('FLAG', 'FLAG{g1t_3xp0sur3_l34ds_t0_cr3d_l34k}')
    return render_template('admin.html', flag=flag)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "version": "1.0.0"})

@app.route('/api/deployments')
def api_deployments():
    return jsonify(DEPLOYMENTS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
