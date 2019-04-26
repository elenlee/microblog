# -*- coding: utf-8 -*-
from app import app, db, avatars
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug import secure_filename
from flask import send_from_directory
from app.forms import PostForm, UploadAvatarForm
from app.models import Post

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,avatar_l='',avatar_s='')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    print(username)
    user = User.query.filter_by(username=username).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('user', username=current_user.username))
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, form=form, posts=posts)

@app.route('/community', methods=['GET'])
@login_required
def community():
    users = User.query.order_by(User.username).all()
    print(users)
    return render_template('community.html', users=users)

@app.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(app.config['AVATARS_SAVE_PATH'], filename)

@app.route('/user/<username>/profile', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = UploadAvatarForm()
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        form.image.data.save(app.config['AVATARS_SAVE_PATH'] + '/' + filename)
        avatar_fname = avatars.crop_avatar(filename, 1, 1, 500, 500)
        user.avatar_l = avatar_fname[2]
        user.avatar_s = avatar_fname[1]
        db.session.commit()
        return redirect(url_for('profile', username=current_user.username, form=form))
    return render_template('profile.html', user=user, form=form)
