from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask import Flask, request, jsonify


# Flask has been included for the potential of extending the project further in the future!
app = Flask(__name__)

engine = create_engine('sqlite:///anime.db')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///anime.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)




# Table schema
class Anime(db.Model):
    anime_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    type = db.Column(db.String(10), nullable=True)
    episodes = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    members = db.Column(db.Integer, nullable=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    anime_id = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)

##Commands kept incase the SQL database needs to be made again
with app.app_context():
        db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
