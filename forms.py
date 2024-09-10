from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,PasswordField,RadioField
from wtforms.validators import DataRequired,equal_to
import pymysql

class NameForm(FlaskForm):
    name=SelectField('您的筛选条件是？',validators=[DataRequired()],choices=[(0,'车型'),(1,'价格'),(2,'品牌'),(3,'车型和价格'),(4,'车型和品牌'),(5,'价格和品牌'),(6,'车型、价格和品牌')],default=6)
    type = SelectField('车型:', validators=[DataRequired()])
    price = SelectField('价格:',choices=[(1,'2w-10w'),(2,'10w-50w'),(3,'50w+')],default=0)
    brand = SelectField('品牌:', validators=[DataRequired()])
    submit=SubmitField('提交')
    def __init__(self,*args,**kwargs):
        super(NameForm, self).__init__(*args,**kwargs)
        conn = pymysql.connect(host='localhost', user='root', password='123456', db='car', charset='utf8',cursorclass = pymysql.cursors.DictCursor)
        cur = conn.cursor()
        cur.execute("SELECT car_class_name FROM car_class ORDER BY CONVERT(car_class_name USING gbk)")
        v = cur.fetchall()
        cur.close()
        self.type.choices = [(i['car_class_name'], i['car_class_name']) for i in v ]
        cur = conn.cursor()
        cur.execute("SELECT car_brand_name FROM car_brand_name")
        v = cur.fetchall()
        cur.close()
        self.brand.choices = [(i['car_brand_name'], i['car_brand_name']) for i in v]
        conn.close()
class LoginForm(FlaskForm):
    username = StringField('请输入您的用户名：', validators=[DataRequired()])
    password=PasswordField('请输入密码：', validators=[DataRequired()])
    submit = SubmitField('登录')
class RegisterForm(FlaskForm):
    username=StringField('请输入用户名：',render_kw={'placeholder':'Please input your username here.'},validators=[DataRequired()])
    password=PasswordField('请输入密码：',render_kw={'placeholder':'Please input your password here.'},validators=[DataRequired(),equal_to('repeat', message='Passwords must match')])
    repeat=PasswordField('重复密码：',render_kw={'placeholder':'Repeat your username here.'})
    gender=RadioField('您的性别：',validators=[DataRequired()],choices=[('F','Female'),('M','Male')])
    age=StringField('您的年龄：',render_kw={'placeholder':'Please input your age here.'})
    submit=SubmitField('注册')