from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# create an instance of flask
app = Flask(__name__)
# create an instance of API
api = Api(app)
# create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# sqlalchemy mapper
db = SQLAlchemy(app)



# add a class
class speechtotext(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fooditemname = db.Column(db.String(80), nullable=False)
    fooditemprice = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"{self.fooditemname} - {self.fooditemprice}"

#For GET request to http://localhost:5000/

class GetItem(Resource):
    def get(self):
        items = speechtotext.query.all()
        item_list = []
        for item in speechtotext:
            item_data = {'Id': item.id, 'FoodItemName': item.fooditemname, 'FoodItemPrice': item.fooditemprice}
            item_list.append(item_data)
        return {"Items": item_list}, 200

# For POST request to http://localhost:5000/item
class AddItem(Resource):
    def post(self):
        if request.is_json:
            item = speechtotext(fooditemname=request.json["FoodItemName"], fooditemprice=request.json["FoodItemPrice"])
            db.session.add(item)
            db.session.commit()
            # return a json response
            return make_response(jsonify({'Id': item.id, 'FoodItemName': item.fooditemname,
                                          'FoodItemPrice': item.fooditemprice}), 201)
        else:
            return {'error': 'Request must be JSON'}, 400

# For PUT request to http://localhost:5000/update/?
class UpdateItem(Resource):
    def put(self, id):
        if request.is_json:
            item = speechtotext.query.get(id)
            if item is None:
                return {'error': 'not found'}, 404
            else:
                item.fooditemname = request.json['FoodItemName']
                item.fooditemprice = request.json['FoodItemPrice']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400

# For DELETE request to http://localhost:5000/delete/?
class DeleteItem(Resource):
    def delete(self, id):
        item = speechtotext.query.get(id)
        if item is None:
            return {'error': 'Not found'}, 404
        db.session.delete(item)
        db.session.commit()
        return f'{id} is deleted', 200

api.add_resource(GetItem, '/')
api.add_resource(AddItem, '/add')
api.add_resource(UpdateItem, '/update/<int:int>')
api.add_resource(DeleteItem, '/delete/<int:int>')

if __name__ == '__main__':
    app.run(debug=True)



