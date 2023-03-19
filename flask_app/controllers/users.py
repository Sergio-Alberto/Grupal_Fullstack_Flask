from flask import render_template, redirect, session, request, flash
from flask_app import app
# DON'T FORGET TO IMPORT REMAINDER OF MODELS!!!
from flask_app.models.user import User
from flask_app.models.producto import Producto
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "celular": request.form['celular'],
        "permiso": request.form['permiso'],
    }
    session['user_id'] = User.add(data)

    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid login credentials","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid login credentials","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    print(user)
    productos = Producto.get_all()

    return render_template("dashboard.html",user=user,productos=productos)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')