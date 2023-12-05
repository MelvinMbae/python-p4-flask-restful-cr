#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# The Api class in Flask-RESTful is responsible for handling the routes and resources in your API. It acts as a container for organizing and managing resources. It allows you to register resources and associate them with specific URL endpoints. This helps in defining the structure of your API and how different resources are accessed.

# Api(app) creates an instance of the Api class, associating it with the Flask app instance.
api = Api(app)

class Home(Resource):
    # Home is a resource class that inherits from Resource, defining the behavior for the '/' endpoint.

    
    def get(self):
        
        response_dict={
            'home':'Welcome to the Newsletter RESTful API',
        }
        
        response= make_response(
            jsonify(response_dict),
            200
        )
        
        return response
    
api.add_resource(Home, '/')

class Newsletters(Resource):
    def get(self):
        response_dict_list = [newsletter.to_dict() for newsletter in Newsletter.query.all()]
        
        response = make_response(
            jsonify(response_dict_list),
            200,
        )
        
        return response
    
    def post(self):
        new_record=Newsletter(
            title = request.form['title'],
            body=request.form['body'],
        )
        
        db.session.add(new_record)
        db.session.commit()
        
        response_dict=new_record.to_dict()
        
        response= make_response(
            jsonify(response_dict),
            201
        )
        return response

# api.add_resource(Newsletters, '/newsletters') registers the Newsletters resource with the Api. It associates the Newsletters resource class with the /newsletters URL endpoint.   
api.add_resource(Newsletters, '/newsletters')

class NewsletterByID(Resource):
    def get(self, id):
        
        # response_dict = Newsletter.query.filter_by(id=id).first().to_dict()

        newsletter_article=Newsletter.query.filter_by(id=id).first()
        
        response_dict=newsletter_article.to_dict()
        response=make_response(jsonify(response_dict),200)
        
        return response
    
    
api.add_resource(NewsletterByID, '/newsletters/<int:id>')
    
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
