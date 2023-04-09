from flask import Flask, request
from flask_restful import Api, Resource, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, current_user, login_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@postgres:5432/postgres"

app.secret_key = 'super_secret_key'

api = Api(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manger = LoginManager()
login_manger.init_app(app)


@login_manger.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


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


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(500), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymouse(self):
        return False

    def get_id(self):
        return self.username

    def __repr__(self):
        return f"<Users {self.id}>"


# Authorization
@app.route("/api/register", methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        hash = generate_password_hash(password)

        if username is None or hash is None:
            abort(400)  # missing argument
        if Users.query.filter_by(username=username).first() is not None:
            abort(400)  # existing user

        user = Users(username=username, password=hash)
        db.session.add(user)
        db.session.commit()

    return {"message": f"user {user.id} has been created successfully"}


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        user = Users.query.filter_by(username = username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return {"message": f"Hellow, {user.username}"}

        return {"message": "invalid password or username"}


# test login required
@app.route('/api/test', methods=['GET'])
@login_required
def hellow_world():
    return {'message': f"Hellow, {current_user.username}!"}




# CRUD operations
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
    app.run(debug=True, host="0.0.0.0", port=5005)
