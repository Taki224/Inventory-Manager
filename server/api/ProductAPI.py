from flask import jsonify, request
from flask_restx import Resource, Namespace
from model.data import shop

ProductAPI = Namespace('product',
                       description='Product Management')



@ProductAPI.route('/categories')
class productCategories(Resource):
    def get(self):
        args = request.args
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        u = shop.authenticate_employee(auth_user, auth_pass)
        if u is not None:
            return jsonify({"categories": shop.getCategories()})

@ProductAPI.route('/create')
class productCreate(Resource):
    def post(self):
        args = request.args
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        new_product = request.json['new_product']
        u = shop.authenticate_employee(auth_user, auth_pass)
        if u is not None:
            if shop.Inventory.checkProduct(new_product['barcode'], new_product['expiration']):
                return jsonify({"success": False})

            barcode = new_product['barcode']
            name = new_product['name']
            category = new_product['category']
            quantity = new_product['quantity']
            expiration = new_product['expiration']
            notifexp = new_product['notifexp']
            notifquan = new_product['notifquan']
            return jsonify({"success": shop.Inventory.newProduct(barcode, name, quantity, category, expiration, notifexp, notifquan, auth_user)})
        else:
            return jsonify({"success": False})

@ProductAPI.route('/<id>')
class SingleProduct(Resource):
    def get(self, id):
        args = request.args
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        u = shop.authenticate_employee(auth_user, auth_pass)
        if u is not None:
            return jsonify({"product": shop.Inventory.getProduct(id)})


@ProductAPI.route('/<id>/updatestock')
class updateStock(Resource):
    def put(self, id):
        args = request.args
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        change = args['change']
        u = shop.authenticate_employee(auth_user, auth_pass)
        if u is not None:
            if shop.Inventory.updateStock(id, change, auth_user):
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})


@ProductAPI.route('/update/<id>')
class UpdateProduct(Resource):
    def put(self, id):
        args = request.args
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        u = shop.authenticate_employee(auth_user, auth_pass)
        if u is not None:
            product = request.json['product']
            return jsonify({"success": shop.Inventory.updateProduct(id, product, auth_user)})

@ProductAPI.route('/delete/<id>')
class DeleteProduct(Resource):
    def delete(self, id):
        args = request.args
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        u = shop.authenticate_employee(auth_user, auth_pass)
        if u is not None:
            return jsonify({"success": shop.Inventory.deleteProduct(id)})

ProductsAPI = Namespace('products',
                       description='Product Management')

@ProductsAPI.route('/')
class productList(Resource):
    def get(self):
        return jsonify({"products": shop.getProducts()})

@ProductsAPI.route('/getnotifications')
class getNotifications(Resource):
    def get(self):
        args = request.args
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        u = shop.authenticate_employee(auth_user, auth_pass)
        if u is not None:
            return jsonify({"notifications": shop.Inventory.getNotifications()})


CategoryAPI = Namespace('category', description='Category Management')

@CategoryAPI.route('/create')
class categoryCreate(Resource):
    def post(self):
        args = request.args
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        new_category = args['name']
        u = shop.authenticate_employee(auth_user, auth_pass)
        if u is not None and u.permission == 1:
            return jsonify({"success": shop.Inventory.addCategory(new_category)})

@CategoryAPI.route('/delete')
class categoryRemove(Resource):
    def delete(self):
        args = request.args
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        category = args['id']
        u = shop.authenticate_employee(auth_user, auth_pass)
        if u is not None and u.permission == 1:
            return jsonify({"success": shop.Inventory.removeCategory(category)})



