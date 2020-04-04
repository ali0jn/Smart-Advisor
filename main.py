from flask import Flask, render_template, url_for, flash, redirect, request

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login/callback')
def callback():
    code = request.args.get("code")
    print(code)

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
