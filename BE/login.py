from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Đặt một secret key bảo mật

bcrypt = Bcrypt(app)

# Giả sử bạn có một bảng users trong SQLite với các trường id, username, password
users = [
    {'id': 1, 'username': 'admin', 'password': bcrypt.generate_password_hash('admin').decode('utf-8')}
]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = next((user for user in users if user['username'] == username), None)

        if user and bcrypt.check_password_hash(user['password'], password):
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')

    return render_template('login.html')

@app.route('/home')
def home():
    return 'Welcome to the home page!'

if __name__ == '__main__':
    app.run(debug=True)