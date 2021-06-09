from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World To Flask'

@app.route('/index')
def index():
    return 'This Is Index Page'

@app.route('/signup')
def signup():
    return '<h3>This Is Signup Page Of Falsk </h3>'

@app.route('/<username>/<int:age>')
def two(username,age):
    if age>=19:
        return f"<h3 style='color:green'> {username} can apply for driving licences </h3>"
    else:
        return f"<h3 style='color:red'> {username} cannot apply for driving licences </h3>"

app.run(debug=True)