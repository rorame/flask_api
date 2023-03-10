from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/postgres"

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Quotes(db.Model):
    __tablename__ = 'quotes'
    # TODO сделать автозаполнение id
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    quote = db.Column(db.String(500), nullable=False)

    def __init__(self, id, author, quote):
        self.id = id
        self.author = author
        self.quote = quote

    def __repr__(self):
        return f"<Quote {self.id}>"


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


@app.route('/quotes', methods=['POST', 'GET'])
def handle_quotes():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_quote = Quotes(id=data['id'], author=data['author'], quote=data['quote'])
            db.session.add(new_quote)
            db.session.commit()
            return {"message": f"quote {new_quote.id} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    # elif request.method == 'GET':
    #     quotes = Quotes.query.all()
    #     results = [
    #         {
    #             "author": quote.author,
    #             "quote": quote.quote,
    #         } for quote in quotes]
    #
    #     return {"count": len(results), "quotes": results}


@app.route('/api', methods=['GET'])
def quotes():
    quotes = Quotes.query.all()
    results = [
        {
            "id": quote.id,
            "author": quote.author,
            "quote": quote.quote,
        } for quote in quotes]

    return {"count": len(results), "quotes": results}


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
