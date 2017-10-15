from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogpass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'kKfY8EBHhJUGFqWmeCXp'

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    body = db.Column(db.String(4000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    posts = Blog.query.all()
    return render_template('blog.html', posts=posts)
    
@app.route('/post', methods=['GET'])
def post():
    form_value = request.args.get('id')
    posts = Blog.query.filter_by(id=form_value)
    return render_template('post.html', posts=posts)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title and body:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/post?id=' + str(new_post.id))
        else:
            flash("Please fill out both the title and body field to create your post", "error")

    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()