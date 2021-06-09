from flask import Flask,render_template,request,make_response,session
import pymysql as sql
from flask_mail import *
import os,random
from datetime import timedelta
import passlib.hash
from passlib.hash import hex_sha1 as sh
from pymysql.connections import DEBUG


# os.environ['Name']='Sachin'
# os.environ.get('Name')

db = sql.connect(host='localhost',port=3306,user='root',database='bankapp')
cur = db.cursor()

app = Flask(__name__)
app.secret_key = "gf3874tyyb84yc58y484bcy$#%$#%$%&^TV*&*&"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('email')
app.config['MAIL_PASSWORD'] = os.environ.get('passwd')
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/')
def header():
    return render_template('header.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route("/aftersignup",methods=['POST'])
def aftersignup():

    name=request.form.get('name')
    passwd = sh.hash(request.form.get('passwd'))
    email = request.form.get('email')
    date =request.form.get('date')
    img=request.files['file']
    img.save(img.filename)
    cur.execute(f"insert into data(name,email,password,date) values('{name}','{email}','{passwd}','{date}')")
    db.commit()
    cur.execute("select * from data order by account desc limit 1")
    data = cur.fetchone()
    d ={
        'Account':data[0],
        'Name':data[1],
        'Email':data[2],
        'Password':data[3],
        'Date':data[4]
    }
    return render_template('aftersignup.html',data=d)

@app.route('/login')
def login():
    
    #if request.cookies.get('account'):
        #return "<h1 style='color:blue'>LOGIN SUCCESSFULL</h1>"
    #else:
        #return render_template('login.html')
    
    if session.get('account'):
        name = session.get('name')
        return render_template('afterlogin.html',name=name)
    else:
        return render_template('login.html')

@app.route("/afterlogin",methods=['POST'])
def afterlogin():
    
    acc=request.form.get('acc')
    passwd = request.form.get('pass')
    cur.execute(f"select account,password,name from data where account={int(acc)}")
    data = cur.fetchone()
    
    if data:
        
        if sh.verify(passwd,data[1]):
            #resp = make_response("<h1 style='color:blue'>LOGIN SUCCESSFULL</h1>")
            #resp.set_cookie('account',acc,30)
            #return resp
            session['account']=acc
            session['name']=data[2]
            return render_template('afterlogin.html',name=data[2])
        
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

@app.route('/logout')
def logout():
    
    #resp = make_response(render_template('header.html',msg='logged out !!!'))
    #resp.delete_cookie('account')
    #return resp
    
    del session['account']
    del session['name']
    return render_template('header.html',msg='logged out !!!')

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/emailvaild',methods=['POST'])
def email():
    email_addr=request.form.get('email')
    session['email']=email_addr
    cur.execute(f"select Email from data where Email='{email_addr}'")
    data = cur.fetchone()
    #print(data)
    #print(data[0])
    if data:
        msg = Message('Validation',sender=os.environ.get('email'),recipients=[data[0]])
        otp=str(random.randint(1111,9999))
        session['otp']=otp
        msg.body = otp
        mail.send(msg)
        return render_template('otp.html',msg="enter otp received on mail")
    else:
        msg = "Email Not Exist!!!"
        return render_template('login.html',data=msg)
@app.route("/afterotp",methods=['POST'])
def afterotp():
    #app.permanent_session_lifetime=timedelta(seconds=30)
    
    otp = request.form.get('otp')
    
    if session.get('otp'):
        if otp == session.get('otp'):
            return render_template('password.html')
        else:
            return render_template('otp.html',msg='invalid otp !!!')
    else:
        return render_template('login.html',data="otp expired")

@app.route('/update_password',methods=['POST'])
def upadte_pwd():
    
    pass1 = request.form.get('pass1')
    pass2 = request.form.get('pass2')
    
    if pass1==pass2:
        cur.execute(f"update data set password='{pass1}' where Email='{session.get('email')}'")
        db.commit()
        return render_template('login.html',data="Password updated successfully")
    else:
        if session.get('otp'):
            return render_template("password.html",msg="confirm password does not match")
        else:
            return render_template('login.html',data="otp expired!!!")


if __name__ == '__main__':
    app.run(debug=True) 