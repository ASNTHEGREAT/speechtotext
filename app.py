from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# create an instance of flask
app = Flask(__name__)
# creating an API object
api = Api(app)
# create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///speechtotext.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# sqlalchemy mapper
db = SQLAlchemy(app)


# add a class
class SpeechToText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fooditemname = db.Column(db.String(80), nullable=False)
    fooditemprice = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"{self.fooditemname} - {self.fooditemprice}"


# For GET request to http://localhost:5000/
class GetItem(Resource):
    def get(self):
        items = SpeechToText.query.all()
        item_list = []
        for i in items:
            item_data = {'Id': i.id, 'FoodItemName': i.fooditemname, 'FoodItemPrice': i.fooditemprice}
            item_list.append(item_data)
        return {"Items": item_list}, 200


# For Post request to http://localhost:5000/item
class AddItem(Resource):
    def post(self):
        if request.is_json:
            item = SpeechToText(fooditemname=request.json['FoodItemName'], fooditemprice=request.json['FoodItemPrice'])
            db.session.add(item)
            db.session.commit()
            # return a json response
            return make_response(
                jsonify({'Id': item.id, 'Food Item Name': item.fooditemname, 'Food Item Price': item.fooditemprice}), 201)
        else:
            return {'error': 'Request must be JSON'}, 400


# For put request to http://localhost:5000/update/?
class UpdateItem(Resource):
    def put(self, id):
        if request.is_json:
            item = SpeechToText.query.get(id)
            if item is None:
                return {'error': 'not found'}, 404
            else:
                item.fooditemname = request.json['FoodItemName']
                item.fooditemprice = request.json['FoodItemPrice']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400


# For delete request to http://localhost:5000/delete/?
class DeleteItem(Resource):
    def delete(self, id):
        item = SpeechToText.query.get(id)
        if item is None:
            return {'error': 'not found'}, 404
        db.session.delete(item)
        db.session.commit()
        return f'{id} is deleted', 200


api.add_resource(GetItem, '/')
api.add_resource(AddItem, '/add')
api.add_resource(UpdateItem, '/update/<int:id>')
api.add_resource(DeleteItem, '/delete/<int:id>')

#
if __name__ == '__main__':
    app.run(debug=True)
