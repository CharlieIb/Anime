from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from flask import Flask, request, jsonify
from Data_processing import recommend_content
from database import db
from front_end_connector import FrontEndConnector

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
# Request the information from the user

## request the list of shows from SQL and show in a drop down menu // automatic fill
with app.app_context():
    result = db.session.execute(text("""
                        SELECT anime_id, name FROM anime WHERE rating > 8 and members > 200000""")).fetchall()


## output to HTML sheet

##In the HTML
## Select min 3 max 10 shows

## Give ratings to these shows 0 - 10

## input from HTML sheet

user_pref = [(1, 'Cowboy Bebop', 1.0), (19, 'Monster', 10.0), (33, 'Berserk', 7.0), (43, 'Ghost in the Shell', 9.5), (5114, 'Fullmetal Alchemist: Brotherhood', 10.0), (6702, 'Fairy Tail', 6.0), (18679, 'Kill la Kill', 6.5), (30276, 'One Punch Man', 7.0), (120, 'Fruits Basket', 10.0)]


## These ratings, along with the user_id are fed back into the below function and recommendations for new shows are produced.
recommend_content = recommend_content(user_pref)


# !!!!! make the below into a function, potentially only one SQL command to increase speed.
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

print(f"Recommended anime content for user: {first}, {second}, {third}")




if __name__ == "__main__":
    fec = FrontEndConnector()
    fec.index()
