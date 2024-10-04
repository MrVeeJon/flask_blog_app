from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from models import User, Post, Comment
from flask_login import login_user, login_required, logout_user, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists, please choose a different one.')
            return redirect(url_for('main.register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('Invalid username or password.')
            return redirect(url_for('main.login'))

        login_user(user)
        flash('Logged in successfully.')
        return redirect(url_for('main.index'))

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))

# Route for creating a new post
@main.route('/create_post', methods=['POST'])
@login_required
def create_post():
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=current_user.id)
    db.session.add(new_post)
    db.session.commit()

    flash('Post created successfully!')
    return redirect(url_for('main.index'))

@main.route('/create_comment/<int:post_id>', methods=['POST'])
@login_required
def create_comment(post_id):
    content = request.form['content']
    post = Post.query.get_or_404(post_id)

    # Create a new comment object
    new_comment = Comment(content=content, user_id=current_user.id, post_id=post.id)
    db.session.add(new_comment)
    db.session.commit()

    flash('Comment added successfully!')
    return redirect(url_for('main.index'))
