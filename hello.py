from flask import  Flask,render_template,url_for,request,session,redirect,flash
from flask_bootstrap import Bootstrap
import pymysql
from forms import NameForm,LoginForm,RegisterForm
from auto_recommend import recommend

app=Flask(__name__)
app.config['SECRET_KEY']='hard to guess'
bootstrap=Bootstrap(app)



@app.route('/result',methods=['GET','POST'])
def show_result():
    if request.method =='GET':
        print(session.get('type'))
        print(session.get('brand'))
        print(session.get('price'))
        conn = pymysql.connect(host='localhost', user='root', password='123456', db='car', charset='utf8',cursorclass = pymysql.cursors.DictCursor)
        def case_0(x):
            cur = conn.cursor()
            cur.execute("SELECT * FROM short_info WHERE car_class='%s'" % (x))
            temp = cur.fetchall()
            cur.close()
            return temp
        def case_1(x):
            if x=='1':
                cur = conn.cursor()
                cur.execute("SELECT * FROM short_info WHERE car_price<10 and car_price>2")
                temp = cur.fetchall()
                cur.close()
                print('2-10')
                return temp
            elif x=='2':
                cur = conn.cursor()
                cur.execute("SELECT * FROM short_info WHERE car_price<50 and car_price>10")
                temp = cur.fetchall()
                cur.close()
                print('10-50')
                return temp
            else:
                cur = conn.cursor()
                cur.execute("SELECT * FROM short_info WHERE car_price>50")
                temp = cur.fetchall()
                cur.close()
                print('50')
                return temp
        def case_2(x):
            cur = conn.cursor()
            cur.execute("SELECT * FROM short_info WHERE car_brand_name='%s'" % (x))
            temp = cur.fetchall()
            cur.close()
            return temp
        def case_3(x,y):
            if y=='1':
                cur = conn.cursor()
                cur.execute("SELECT * FROM short_info WHERE car_class='%s' and car_price<10 and car_price>2" % (x))
                temp = cur.fetchall()
                cur.close()
                print('2-10')
                return temp
            elif y=='2':
                cur = conn.cursor()
                cur.execute("SELECT * FROM short_info WHERE car_class='%s' and car_price<50 and car_price>10" % (x))
                temp = cur.fetchall()
                cur.close()
                print('10-50')
                return temp
            else:
                cur = conn.cursor()
                cur.execute("SELECT * FROM short_info WHERE car_class='%s' and car_price>50 " % (x))
                temp = cur.fetchall()
                cur.close()
                print('50')
                return temp
        def case_4(x,z):
            cur = conn.cursor()
            cur.execute("SELECT * FROM short_info WHERE car_class='%s' and car_brand_name='%s' " % (x,z))
            temp = cur.fetchall()
            cur.close()
            return temp
        def case_5(y,z):
            if y=='1':
                cur = conn.cursor()
                cur.execute("SELECT * FROM short_info WHERE car_price<10 and car_price>2 and car_brand_name='%s'" % (z))
                temp = cur.fetchall()
                cur.close()
                print('2-10')
                return temp
            elif y=='2':
                cur = conn.cursor()
                cur.execute("SELECT * FROM short_info WHERE car_price<50 and car_price>10 and car_brand_name='%s'" % (z))
                temp = cur.fetchall()
                cur.close()
                print('10-50')
                return temp
            else:
                cur = conn.cursor()
                cur.execute("SELECT * FROM short_info WHERE car_price>50 and car_brand_name='%s'" % (z))
                temp = cur.fetchall()
                cur.close()
                print('50')
                return temp
        def case_6(x,y,z):
            if y=='1':
                cur = conn.cursor()
                cur.execute("SELECT * FROM short_info WHERE car_class='%s' and car_price<10 and car_price>2 and car_brand_name='%s'" % (
                x, z))
                temp = cur.fetchall()
                cur.close()
                print('2-10')
                return temp
            elif y=='2':
                cur = conn.cursor()
                cur.execute("SELECT * FROM short_info WHERE car_class='%s' and car_price<50 and car_price>10 and car_brand_name='%s'" % (
                x, z))
                temp = cur.fetchall()
                cur.close()
                print('10-50')
                return temp
            else:
                cur = conn.cursor()
                cur.execute("SELECT * FROM short_info WHERE car_class='%s' and car_price>=50 and car_brand_name='%s'" % (
                x, z))
                temp = cur.fetchall()
                cur.close()
                print('50')
                return temp
        # w = case_6(session.get('type'), session.get('price'), session.get('brand'))
        if session.get('name')=='0':
            w=case_0(session.get('type'))
        if session.get('name')=='1':
            w=case_1(session.get('price'))
        if session.get('name')=='2':
            w=case_2(session.get('brand'))
        if session.get('name')=='3':
            w=case_3(session.get('type'),session.get('price'))
        if session.get('name')=='4':
            w=case_4(session.get('type'),session.get('brand'))
        if session.get('name')=='5':
            w=case_5(session.get('price'),session.get('brand'))
        if session.get('name')=='6':
            w=case_6(session.get('type'),session.get('price'),session.get('brand'))
        conn.close()
        return render_template('index.html',name=session.get('name'),w=w)
    else:return render_template('hello.html')

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='GET':
        nameForm=NameForm()
        return render_template('index2.html',form=nameForm)
    else:
        nameForm=NameForm()
    # if nameForm.validate_on_submit():
        session['name'] = nameForm.name.data
        session['type'] = nameForm.type.data
        session['price'] = nameForm.price.data
        session['brand'] = nameForm.brand.data
        nameForm.name.data = ''
        nameForm.type.data = ''
        nameForm.price.data = ''
        nameForm.brand.data = ''
        return redirect(url_for('show_result'))

@app.route('/info/<name>',methods=['GET'])
def info(name):
    session['car_type_name']=name
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='car', charset='utf8',cursorclass = pymysql.cursors.DictCursor)
    cur = conn.cursor()
    cur.execute("SELECT * FROM long_info WHERE car_type_name='%s'" % (session.get('car_type_name')))
    detail_info = cur.fetchall()
    cur.close()
    cur=conn.cursor()
    cur.execute("SELECT car_type_ID FROM long_info WHERE car_type_name='%s'" % (session.get('car_type_name')))
    temp=cur.fetchall()
    #temp_num = None  # 初始化 temp_num 以避免未赋值错误
    for i in temp:
        temp_num=i['car_type_ID']
        print(temp_num)
    cur.close()
    conn.close()
    re_point=recommend(temp_num)
    print(re_point)
    return render_template('hello.html',name=name,detail_info=detail_info,re_point=re_point)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        loginForm=LoginForm()
        return render_template('login.html',form=loginForm)
    else:
        loginForm=LoginForm()
        # l_rForm=L_RForm()
        if loginForm.validate_on_submit():
            session['username']=loginForm.username.data
            session['password']=loginForm.password.data
            conn = pymysql.connect(host='localhost', user='root', password='123456', db='car', charset='utf8',cursorclass = pymysql.cursors.DictCursor)
            cur = conn.cursor()
            cur.execute("SELECT username FROM user_info WHERE username='%s' and password='%s'" %(session.get('username'),session.get('password')))
            u_info = cur.fetchall()
            cur.close()
            conn.close()
            if u_info == ():
                flash('用户名或密码错误!')
                return redirect(url_for('login'))
            else:
                for i in u_info:
                    session['username']=i['username']
                return redirect(url_for('userview',username=session.get('username')))
        else:return redirect(url_for('login'))
        # return redirect(url_for('index'))

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        registerForm=RegisterForm()
        return render_template('register.html',form=registerForm)
    else:
        registerForm=RegisterForm()
        # if registerForm.validate_on_submit():
        session['temp_username']=registerForm.username.data
        session['temp_password']=registerForm.password.data
        session['temp_gender']=registerForm.gender.data
        session['temp_age']=registerForm.age.data
        conn = pymysql.connect(host='localhost', user='root', password='123456', db='car', charset='utf8')
        cur = conn.cursor()
        cur.execute("SELECT username FROM user_info WHERE username='%s'" % (session.get('temp_username')))
        u_name = cur.fetchall()
        cur.close()
        if u_name != ():
            flash('该用户已存在!')
            conn.close()
            return redirect(url_for('register'))
        else:
            cur=conn.cursor()
            cur.execute("INSERT INTO user_info(username,password,gender,age) VALUES('%s','%s','%s','%s')" % (session.get('temp_username'),session.get('temp_password'),session.get('temp_gender'),session.get('temp_age')))
            conn.commit()
            conn.close()
            flash('注册成功！')
            return redirect(url_for('login'))
    return redirect(url_for('index'))

@app.route('/user/<username>',methods=['GET','POST'])
def userview(username):
    return render_template('user_page.html',username=username)
if __name__=='__main__':
    app.run(debug=True)
