from flask import Flask,render_template,request
import pymysql as sql

db = sql.connect(host='localhost',port=3306,user='root',database='bankapp')
cur =db.cursor()

app = Flask(__name__)

@app.route('/')
def header():
    return render_template('header.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route("/aftersignup",methods=['POST'])
def aftersignup():

    name=request.form.get('name')
    passwd = request.form.get('passwd')
    email = request.form.get('email')
    date =request.form.get('date')
    img=request.files['file']
    img.save(img.filename)
    cur.execute(f"insert into data(name,email,password,date) values('{name}','{email}','{passwd}','{date}')")
    db.commit()
    cur.execute("select * from data order by account desc limit 1")
    data = cur.fetchone()
    d = {
        'Account':data[0],
        'Name':data[1],
        'Email':data[2],
        'Password':data[3],
        'Date':data[4]
    }
    return render_template('aftersignup.html',data=d)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/afterlogin",methods=['POST'])
def afterlogin():
    acc=request.form.get('acc')
    passwd = request.form.get('pass')
    cur.execute(f"select account,password from data where account={int(acc)}")
    data = cur.fetchone()
    
    if data:
        if passwd==data[1]:
            return "<h1 style='color:blue'>LOGIN SUCCESSFULL</h1>"
        else:
            
            msg = "Invalid Password..."
            return render_template('login.html',data=msg)
    else:
        msg = "Account not exist..."
        return render_template('login.html',data=msg)

@app.route('/check/<name>/<int:age>')
def jinja(name,age):
    return render_template('jinja.html',name=name,age=age)

@app.route('/one')
def one():
    return render_template('jinja.html',data={'Name':'Samyak','Course':'DS'})

if __name__ == '__main__':
    app.run(debug=True)