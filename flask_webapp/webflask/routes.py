from flask import url_for,redirect,render_template,flash,request
from webflask import app,db,bcrypt
from webflask.forms import RegistrationForm,LoginForm,UpdateUsernameForm,UpdateEmailForm,PostForm
from webflask.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required

@app.route("/")
@app.route("/home",methods=["GET","POST"])
def home():
    form=PostForm()
    priv_posts=[]
    if request.method=="POST" and  current_user.is_authenticated:
        post=Post(title=form.title.data,content=form.text.data,private=form.private.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("your post has been created","success")
        return redirect(url_for('home'))
    elif request.method=="POST" and not current_user.is_authenticated:   
        flash("login to add posts","danger")
        return redirect(url_for('login'))
    else:
        if current_user.is_authenticated:
            priv_posts=Post.query.filter_by(private=True,user_id=current_user.id).all()
        Posts=Post.query.filter_by(private=False).all()
        return render_template("home.html", title='home',form=form,Posts=Posts,priv_posts=priv_posts)

@app.route("/registre",methods=['GET','POST'])
def registre():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pw=bcrypt.generate_password_hash(form.password.data).decode()
        user=User(username=form.username.data,email=form.email.data,password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account have been created you can now login!",'success')
        return redirect(url_for('login'))
    return render_template("register.html",title='register',form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("check email or password","danger")
    return render_template("login.html",title='login',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateUsernameForm()
    form1 = UpdateEmailForm()
    username=current_user.username
    email=current_user.email
    if request.method=="POST":
        if form.username.data!=None and form.username.data!=username:
            user=User.query.filter_by(username=form.username.data).first()
            if user:
                flash("the username is taken. please choose another one","danger")
                return redirect(url_for('account'))
            else:
                username=form.username.data
        if form1.email.data!=None and form1.email.data!=email:
            user=User.query.filter_by(email=form1.email.data).first()
            if user:
                flash("the email is taken. please choose another one","danger")
                return redirect(url_for('account'))
            else:
                email=form1.email.data
        if username != current_user.username or email!=current_user.email:
            current_user.username=username
            current_user.email=email
            db.session.commit()
            flash("updated successfuly", "success")
        return redirect(url_for('account'))

    if request.method == "GET":
        form.username.data = current_user.username
        form1.email.data = current_user.email
    
    image_file =  url_for('static',filename='img/default.jpg')  
    return render_template("account.html", title="My Account",image_file=image_file, form=form, form1=form1)

@app.route("/about",methods=["GET"])
def about():
    return render_template("about.html",title="about")

@app.route("/post/<int:post_id>",methods=["GET"])
@login_required
def post(post_id):
    post = Post.query.filter(
    (Post.id == post_id) &
    ((Post.user_id == current_user.id) | (Post.private == False))
).first_or_404()
    return render_template("post.html",title=post.title,post=post)

@app.route("/post/<int:post_id>/update",methods=["GET","POST"])
@login_required
def post_update(post_id):
    form=PostForm()
    post = Post.query.filter(
    (Post.id == post_id) &
    (Post.user_id == current_user.id)
).first_or_404()
    if request.method=="POST" and form.validate_on_submit:
        post.title=form.title.data
        post.content=form.text.data
        post.private=form.private.data
        db.session.commit()
        flash("your post has been updated","success")
        return redirect(url_for('post',post_id=post.id))
    elif request.method=="GET":
        form.title.data=post.title
        form.text.data=post.content
        form.private.data=post.private
    return render_template("post_update.html",title=post.title,post=post,form=form)

@app.route("/post/<int:post_id>/delete",methods=["POST"])
@login_required
def post_delete(post_id):
    post = Post.query.filter(
    (Post.id == post_id) &
    (Post.user_id == current_user.id)).first_or_404()
    db.session.delete(post)
    db.session.commit()
    flash("your post has been deleted","success")
    return redirect(url_for('home'))