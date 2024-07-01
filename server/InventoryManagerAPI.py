from flask import Flask
from flask_restx import Api
from api.EmployeeAPI import EmployeeAPI, EmployeesAPI
from api.ProductAPI import ProductAPI, ProductsAPI, CategoryAPI
from util.json_utils import InventoryJsonEncoder


inventoryApp = Flask(__name__)

# need to extend this class for custom objects, so that they can be jsonified
inventoryApp.json_encoder = InventoryJsonEncoder
inventoryAPI = Api(inventoryApp, version='1.0', title='InventoryManagerAPI',
                   contact_email = "22IMC10262@fh-krems.ac.at",
                   description='Inventory Manager API')

# Add all the parts of the API here
inventoryAPI.add_namespace(EmployeeAPI)
inventoryAPI.add_namespace(EmployeesAPI)
inventoryAPI.add_namespace(ProductAPI)
inventoryAPI.add_namespace(ProductsAPI)
inventoryAPI.add_namespace(CategoryAPI)

if __name__ == '__main__':
    inventoryApp.run(debug=True, port=7890)
