from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Producto:

    db_name = "users_productos" # cambiar después

    def __init__(self,data):
        self.id = data['id']
        self.denominacion = data['denominacion'] # cambiar por tabla normalizada
        self.cantidad = data['cantidad']
        self.precio = data['precio']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        #self.nombre_producto_id = data['nombre_producto_id'] # cuando esté la tabla normalizada
        self.creator = None
        self.users_who_voted = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM productos"
        results = connectToMySQL(cls.db_name).query_db(query)
        return results

    @classmethod 
    def create_producto(cls, data):
        query = "INSERT INTO productos (denominacion, cantidad, precio, user_id) VALUES (%(denominacion)s, %(cantidad)s, %(precio)s, %(user_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM productos WHERE id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update_producto(cls, data):
        #SE AGREGÓ updated_at, ver si funciona
        query = "UPDATE productos SET denominacion = %(denominacion)s, cantidad = %(cantidad)s, precio = %(precio)s, updated_at = NOW() WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def vote(cls, data):
        query = "INSERT INTO votes (user_id, producto_id) VALUES (%(user_id)s, %(producto_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    
    @classmethod
    def remove_vote(cls, data):
        query = "DELETE FROM votes WHERE user_id = %(user_id)s AND producto_id = %(producto_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def get_all_voted_productos(cls, data):
        productos_voted = []
        query = "SELECT producto_id FROM votes JOIN users ON users.id = user_id WHERE user_id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        for result in results:
            productos_voted.append(result['producto_id'])
        return productos_voted

    @classmethod
    def show_all_productos(cls):
        query = "SELECT productos.denominacion, productos.cantidad,productos.precio,users.first_name, productos.id, COUNT(votes.producto_id) AS votes FROM productos "\
        "LEFT JOIN users ON users.id = productos.user_id "\
        "LEFT JOIN votes ON productos.id = votes.producto_id "\
        "GROUP by productos.id "\
        "ORDER BY COUNT(votes.producto_id) DESC;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        return results
    
    
    @classmethod
    def destroy_producto(cls, data):
        query = "DELETE FROM productos WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @staticmethod
    def validate_producto(producto):
        is_valid = True
        if len(producto['denominacion']) < 1:
            is_valid = False
            flash("Name field can not be left blank","producto")
        if len(producto['cantidad']) < 0:
            is_valid = False
            flash("Filling field can not be left blank","producto")
        if len(producto['precio']) < 0:
            is_valid = False
            flash("Crust field can not be left blank","producto")
        return is_valid

    @classmethod
    def get_producto_and_user(cls, data):
        query = "SELECT * FROM productos LEFT JOIN users ON users.id = productos.user_id WHERE productos.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

