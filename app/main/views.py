from flask import Flask, render_template, request, url_for, session, redirect
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email

@main.route('/',methods=['GET','POST'])
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
            send_email('383789543@qq.com', "new_user", 'mail/new_user', user=user)
        else:
            session['known'] = True
        # old_name = session.get('name')
        # if old_name != form.name.data:
        #   flash('looks like you have changed your name')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',form=form, name=session.get('name'),known=session.get('known',False))