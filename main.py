from flask import Flask, render_template, url_for
app = Flask(__name__)

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
def hello():
    return render_template('home.html', posts=data)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
