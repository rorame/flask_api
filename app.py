from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# TODO довести до ума конфиги для postgres
# app.config['SQLALCHEMY_DATABASE_URI'] =

api = Api(app)
db = SQLAlchemy(app)


class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    quote = db.Column(db.String(500), nullable=False)


# with app.app_context():
#     db.create_all()

quotes = [
    {
        "id": 0,
        "author": "Kevin Kelly",
        "quote": "The business plans of the next 10,000 startups are easy to forecast: " +
                 "Take X and add AI."
    },
    {
        "id": 1,
        "author": "Stephen Hawking",
        "quote": "The development of full artificial intelligence could " +
                 "spell the end of the human race… " +
                 "It would take off on its own, and re-design " +
                 "itself at an ever increasing rate. " +
                 "Humans, who are limited by slow biological evolution, " +
                 "couldn't compete, and would be superseded."
    }]


class Quote(Resource):
    def get(self, id):
        for q in quotes:
            if q["id"] == id:
                return q, 200
            return "Quote not found", 404

    # TODO допилить пост запрос
    # def post(self, id):
    #     parser = reqparse.RequestParser
    #     parser.add_argument('author')
    #     parser.add_argument('quote')
    #     params = parser.parse_args()
    #
    #     for q in quotes:
    #         if q['id'] == id:
    #             return f"Quote with {id} already exist", 400
    #
    #     quote = {
    #         'id': id
    #     }



class QuoteList(Resource):
    def get(self):
        return quotes, 200


api.add_resource(Quote, '/api/<int:id>')
api.add_resource(QuoteList, '/api/')

if __name__ == "__main__":
    app.run(debug=True)
