from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from flask import Flask, request, jsonify
from Data_processing import recommend_content
from database import db

# Flask has been included for the potential of extending the project further in the future!

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///anime.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    return app

# Table schema - left for reference
'''class Anime(db.Model):
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
        db.create_all()'''

# Initialise the app
app = create_app()

recommend_content = recommend_content(30)

first_rec = recommend_content[0]
second_rec = recommend_content[1]
third_rec = recommend_content[2]
with app.app_context():
    first = db.session.execute(text("SELECT name FROM anime WHERE anime_id = :first_rec"),
                           {"first_rec" : first_rec}).fetchone()

    second = db.session.execute(text("SELECT name FROM anime WHERE anime_id = :second_rec"),
                           {"second_rec" : second_rec}).fetchone()

    third = db.session.execute(text("SELECT name FROM anime WHERE anime_id = :third_rec"),
                           {"third_rec" : third_rec}).fetchone()

print(f"Recommended anime content for user 500: {first}, {second}, {third}")




if __name__ == "__main__":
    app.run(debug=True)
