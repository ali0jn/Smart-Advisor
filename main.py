from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '007'

data = [
    {
        'course_code': 'CS 202',
        'course_name': 'Advanced Algorithms',
        'instructor': 'Mehmet Baysan',
        'classroom': 'AB4 4301'
    },
    {
        'course_code': 'CS 350',
        'course_name': 'Database Systems',
        'instructor': 'Ali Cakmak',
        'classroom': 'AB4 4301'
    },
    {
        'course_code': 'CS 240',
        'course_name': 'Exploratory Data Analysis',
        'instructor': 'Baris Arslan',
        'classroom': 'AB5 5301'
    }
]


@app.route('/')
def home():
    return render_template('home.html', posts=data)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form='form')

if __name__ == '__main__':
    app.run(debug=True)
