
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '53e64drytfgyilvaz'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    #Blog_entry_id = db.Column(db.Integer, db.ForeignKey(Blog_entry_id))

    def __init__ (self, title, body):
        self.title = title
        self.body = body
       

@app.route('/newpost', methods = ['POST', 'GET']) 
def blog():
    if request.method == 'POST':
       
        blog_title = request.form['title']
        blog_body = request.form['body']
        blog = Blog(blog_title, blog_body)
        blog_title_error = ""
        blog_body_error = "" 
        if len(blog_title)>120:
            blog_title_error = "Title too long"
            
        if len(blog_body)>1000:
            blog_body_error = "Body too long"
            
        if len(blog_title) <=0:
            blog_title_error = "Title can't be empty"
           
        if len(blog_body) <=0:
            blog_body_error = "Body can't be empty"
                    
        if not blog_title_error and not blog_body_error: 
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog?id={0}'.format(new_blog.id))
        else:
            return render_template('newpost.html', blog_title_error=blog_title_error, blog_body_error=blog_body_error)
    if request.method == 'GET':
        return render_template('newpost.html')

@app.route('/blog', methods=['GET'])
def index():
    if request.args.get("id"):
        blogger = Blog.query.filter_by(id = request.args.get("id")).first()
        return render_template('newtemplate.html', blogger=blogger)

    else:    
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)            


if __name__== '__main__':
    app.run()





