from flask import render_template,redirect,session,request, flash
from flask_app import app 
from flask_app.models.producto import Producto
from flask_app.models.user import User


@app.route('/create/producto',methods=['POST'])
def create_producto():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Producto.validate_producto(request.form):
        return redirect('/dashboard')
    data = {
        "denominacion": request.form["denominacion"],
        "cantidad": request.form["cantidad"],
        "precio": request.form["precio"],
        "user_id": session["user_id"]
    }
    Producto.create_producto(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_producto(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }

    edit=Producto.get_one(data)
    
    return render_template("edit.html",edit=edit)

@app.route('/delete/producto/<int:id>')
def delete_producto(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id,
        "producto_id": id
    }
    Producto.destroy_producto(data)
    return redirect('/dashboard')

@app.route('/update/producto/<int:id>',methods=['POST'])
def update_producto(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Producto.validate_producto(request.form):
        return redirect(f'/edit/{id}')
    
    data = {
        "denominacion": request.form["denominacion"],
        "cantidad": request.form["cantidad"],
        "precio": request.form["precio"],
        "id": id
    }
    
    Producto.update_producto(data)
    return redirect('/dashboard')

@app.route('/productos')
def show_productos():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    user = User.get_by_id(data)
    productos = Producto.show_all_productos()
    return render_template('productos.html',productos=productos,user=user)

@app.route('/show/<int:id>')
def show_producto(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    
    producto=Producto.get_one(data)
    vote_producto=Producto.get_all_voted_productos(user_data)
    user = Producto.get_producto_and_user(data)[0]

    return render_template("show.html",producto=producto,vote_producto=vote_producto,user=user)

@app.route('/vote/<int:id>')
def like(id):
    data = {
        "user_id": session['user_id'],
        "producto_id": id
        }
    Producto.vote(data)
    return redirect('/productos') 

@app.route('/remove_vote/<int:id>')
def unlike(id):
    data = {
        "user_id": session['user_id'],
        "producto_id": id
        }
    Producto.remove_vote(data)
    return redirect('/productos')






