from flask import Flask ,render_template,request,redirect,url_for,flash
import pymysql

app = Flask(__name__) #creating the Flask class object   
app.config['SECRET_KEY'] = "kjboujbjub"

m1 =35
m2 =35
m3 =35
m4 =35
ussr='jh'

conn = pymysql.connect( 
	host='localhost', 
	user='root', 
	password = "", 
	db='MOVIE', 
	) 
	
cur = conn.cursor()


@app.route('/',methods=['GET','POST']) 
def login():
    global ussr
    import datetime
    current_date = datetime.date.today()
    cur.execute(f"delete from detials where date < '{current_date}';")
    conn.commit()
    if request.method == 'POST':
        usr = request.form.get("email")
        ussr=usr        
        print(usr)
        pswrd = request.form.get("password")
        print(pswrd)
        cur.execute(f"select password from users where email ='{usr}';")
        res = cur.fetchall()
        if len(res)==0:
            flash("Username not valid")
            return redirect(url_for('create'))
        if pswrd==res[0][0]:
            if ussr=="admin@a5":
                return redirect(url_for('admin'))
            else :
                return redirect(url_for('new'))
        else:
            flash("Password invalid")
            return redirect(url_for('login'))

    return  render_template("login.html")


@app.route('/new',methods=['GET','POST'])    
def new():  
    return  render_template("new.html")

@app.route('/ex',methods=['GET','POST']) 
def ex():  
    return  render_template("ex.html")


@app.route('/success',methods=['GET','POST'])    
def success():  
    #import random
    #x=random.randrange(100000,999999)
    return  render_template("success.html",id=idd)


@app.route('/book/<name>',methods=['GET','POST']) 
def book(name):  
    if name=='OPPENHEIMER':
        im='oppn.jpg'
    elif name=='FIGHTCLUB':
        im='fc.jpg'
    elif name=='INERSTELLAR':
        im='inter.jpg'
    elif name=='JOHNWICK4':
        im='jw.jpg'
    global ussr
    import datetime
    current_date = datetime.date.today()
    print(ussr)
    
    if request.method == 'POST':
        cur.execute(f"select email from users where email='{ussr}';")
        data = cur.fetchall()
        if len(data)>0:
            print("user=",data[0][0])
            time=request.form.get("time")
            print(time)
            dte = request.form.get("dte").split(" ")[0]
            print(dte)
            seats=request.form.get("seatsno")
            print("read value",seats)
            cur.execute(f"select sum(seats) from detials where movie='{name}' and date='{dte}' and time='{time}';")
            p = cur.fetchone()
            k=p[0]
            k = k if k is not None else 0
            print("total seats",p[0])
            if k>=45:
                flash("Booking full ")
                
            elif (int(k) + int(seats)) >= 45:
                flash('Selected no. of seats not available')
                
            else:
                cur.execute(f"select seats from detials where email ='{ussr}' and movie ='{name}' and time ='{time}' and date='{dte}';")
                res = cur.fetchall()
                global idd
                import random
                x=random.randrange(100000,999999)
                idd = x
                if len(res)>0:
                    print("resoo",res[0][0])
                    num=res[0][0]
                    num = num if num is not None else 0
                    print("num",num)
                    seats = int(seats) + num
                    print("seats after",seats)
                    amt = int(seats) * 177
                    cur.execute(f"update detials set seats = {seats} where email = '{ussr}' and movie ='{name}' and time ='{time}' and date='{dte}';")
                    cur.execute(f"insert into transactions values ('{x}','{dte}','{time}',{amt},'{name}');")
                    conn.commit()
                else:
                    amt = int(seats) * 177
                    cur.execute(f"insert into detials values ('{ussr}','{time}','{dte}',{seats},'{name}');")
                    cur.execute(f"insert into transactions values ('{x}','{dte}','{time}',{amt},'{name}');")
                    conn.commit()

                return redirect(url_for('success'))
        else:
            flash("User timed out. Login again")
            return redirect(url_for('login'))
    return  render_template("book.html", current_date=current_date,img=im)


@app.route('/create',methods=['GET','POST'])   
def create():
    global ussr
    if request.method == 'POST':
        usr = request.form.get("email")
        print(usr)
        ussr=usr
        name = request.form.get("name")
        psd = request.form.get("password")
        cur.execute(f"select password from users where email ='{usr}';")
        res = cur.fetchall()
        if len(res)==0:
            cpsd = request.form.get("confirmPassword")
            if psd==cpsd:
                cur.execute(f"insert into users values ('{usr}','{name}','{psd}');")
                conn.commit()
                flash("New user created")
                return redirect(url_for('new'))
            else :
                flash("Password not matched")
        else:
            flash("User already exist")
            return redirect(url_for('login'))
    return  render_template("create.html")


@app.route('/home')
def home():
    cur.execute(f"select name from users where email='{ussr}';")
    data=cur.fetchone()
    cur.execute(f"select time,date,seats,movie from detials where email='{ussr}';")
    na=cur.fetchall() 
    
    return render_template("home.html",na=na,user=ussr,data=data[0])

@app.route('/admin')
def admin():
    cur.execute(f"select name from users where email='{ussr}';")
    data=cur.fetchone()
    cur.execute(f"select * from transactions;")
    na=cur.fetchall() 
    return render_template("admin.html",na=na,user=ussr,data=data[0])

@app.route('/delete',methods=['GET','POST'])
def delete():
    de = request.form.get("tid")
    if de is not None:
        cur.execute(f"select tid from transactions where tid={de};")
        res = cur.fetchall()
        if len(res)==0:
            flash("No such transaction found")
            return redirect(url_for('delete'))
        else:
            cur.execute(f"delete from transactions where tid={de};")
            conn.commit()
            flash("Transaction deleted successfully")
    return render_template("delete.html")

if __name__ =='__main__':
    app.run(debug = True)
