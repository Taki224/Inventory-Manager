from flask import jsonify, request
from flask_restx import Resource, Namespace

from model.Employee import Employee
from model.data import shop

EmployeeAPI = Namespace('employee',
                        description='Employee Management')

from hashlib import sha256

def hash(input):
    return sha256(input.encode('utf-8')).hexdigest()


@EmployeeAPI.route('/login')
class employeeLogin(Resource):
    def post(self):
        args = request.args
        username = args['username']
        password = args['password']
        user = shop.authenticate_employee(username, password)
        # Check if username and password are valid
        if user is not None and user.permission != 2:
            return jsonify({"message": "Login successful!", "user": user.to_json()})
        else:
            return jsonify({"message": "Invalid username or password or user suspended!"})

@EmployeeAPI.route('/changepassword')
class employeeChangePassword(Resource):
    def put(self):
        args = request.args
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        new_password = args['new_password']
        u = shop.authenticate_employee(auth_user, auth_pass)
        if u is not None:
            if auth_pass == args['old_password'] == u.password:
                shop.update_employee_password(u.id, new_password)
                return jsonify({"message": "Password changed successfully!"})

@EmployeeAPI.route('/changeemail')
class employeeChangeEmail(Resource):
    def put(self):
        args = request.args
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        new_email = args['new_email']
        u = shop.authenticate_employee(auth_user, auth_pass)
        if u is not None:
            shop.update_employee_email(u.id, new_email)
            return jsonify({"message": "Email changed successfully!"})



@EmployeeAPI.route('/create')
class employeeCreate(Resource):
    def post(self):
        args = request.args
        username = args['username']
        email = args['email']
        password = args['password']
        genpassword = args['password']
        permission = 1 if args['is_admin'] == "True" else 0
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        u = shop.authenticate_employee(auth_user, auth_pass)
        if shop.employee_by_username(username) is not None:
            return jsonify({"message": "username_exists"})
        if u is not None and u.permission == 1:
            shop.create_employee(username, email, password, genpassword, permission, auth_user)
            return jsonify({"message": "Employee created successfully!"})

@EmployeeAPI.route('/<id>')
class employee(Resource):
    def get(self, id):
        args = request.args
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        u = shop.authenticate_employee(auth_user, auth_pass)
        if u is not None and u.permission == 1:
            for e in shop.employees:
                if e.id == int(id):
                    return jsonify(e.to_json())
            return jsonify({"message": "Employee not found!"})

    def put(self, id):
        args = request.args
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        u = shop.authenticate_employee(auth_user, auth_pass)
        if u is not None and u.permission == 1:
            shop.update_employee(id, args, auth_user)
            return jsonify({"message": "Employee updated successfully!"})


EmployeesAPI = Namespace('employees',
                        description='Employee Management')

@EmployeesAPI.route('/')
class employeeList(Resource):
    def get(self):
        args = request.args
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        return jsonify([e.to_json() for e in shop.employees])

@EmployeesAPI.route('/getchanges')
class employeeList(Resource):
    def get(self):
        args = request.args
        auth_user = args['auth_user']
        auth_pass = args['auth_password']
        if shop.authenticate_employee(auth_user, auth_pass) is not None:
            return jsonify({"changes": shop.getChanges()})