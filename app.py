from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/postgres"

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Quotes(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    quote = db.Column(db.String(500), nullable=False)

    def __init__(self, id, author, quote):
        self.id = id
        self.author = author
        self.quote = quote

    def __repr__(self):
        return f"<Quote {self.id}>"


class QuoteList(Resource):
    def get(self):
        quotes = Quotes.query.all()
        results = [
            {
                "id": quote.id,
                "author": quote.author,
                "quote": quote.quote,
            } for quote in quotes]
        return results, 200

    def post(self):
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                new_quote = Quotes(id=data['id'], author=data['author'], quote=data['quote'])
                db.session.add(new_quote)
                db.session.commit()
                return {"message": f"quote {new_quote.id} has been created successfully."}
            else:
                return {"error": "The request payload is not in JSON format"}

    def delete(self, id):
        quote = Quotes.query.get_or_404(id)
        db.session.delete(quote)
        db.session.commit()
        return {"message": f"quote {quote.id} successfully deleted"}

    def put(self, id):
        quote = Quotes.query.get_or_404(id)
        data = request.get_json()
        quote.author = data['author']
        quote.quote = data['quote']
        db.session.add(quote)
        db.session.commit()
        return {"message": f"quote {quote.id} successfully updated"}


api.add_resource(QuoteList, '/api/', '/api/<int:id>')

if __name__ == "__main__":
    app.run(debug=True)
