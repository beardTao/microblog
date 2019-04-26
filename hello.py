from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

from flask_mail import Mail, Message
from threading import Thread

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data2.splite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#配置邮箱信息
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = os.environ.get('mail_username')
app.config['MAIL_PASSWORD'] = os.environ.get('mail_password')
print(app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD'])
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[TAO]'
app.config['FLASKY_MAIL_SENDER'] = 'beardtao@163.com'

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate =Migrate(app, db)
mail = Mail(app)

def send_async_mail(app, msg):
	with app.app_context():
		mail.send(msg)

def send_mail(to, subject, template, **kwargs):
	msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
	msg_body = render_template(template + '.txt',**kwargs)
	msg.html = render_template(template + '.html',**kwargs)
	thr = Thread(target=send_async_mail, args=[app, msg])
	thr.start()
	return thr

class NameForm(FlaskForm):
	name = StringField('name:', validators=[DataRequired()])
	submit = SubmitField('Submit')

class Role(db.Model):
	__tablename__ = 'roles'#表名
	id = db.Column(db.Integer, primary_key=True)#表属性
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__ = 'users'#表名
	id = db.Column(db.Integer, primary_key=True)#表属性
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username

@app.route('/',methods=['GET','POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		print(user)
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			db.session.commit()
			session['known'] = False
			send_mail('383789543@qq.com', "new_user", 'mail/new_user', user=user)
		else:
			session['known'] = True
		# old_name = session.get('name')
		# if old_name != form.name.data:
		# 	flash('looks like you have changed your name')
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html',form=form, name=session.get('name'),known=session.get('known',False))

@app.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)

