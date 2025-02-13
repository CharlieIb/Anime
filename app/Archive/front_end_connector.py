# from flask import Flask, jsonify, render_template, request
# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
# from app.data_processing import recommend_content
# from jinja2 import StrictUndefined
#
# # Initialise the database
# class FrontEndConnector:
#     db = SQLAlchemy()
#     def __init__(self):
#         # Initialise the app
#         self.app = Flask(__name__)
#
#         #
#         self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/anime.db"
#         self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#
#         # Initialise the database with the app
#         self.db.init_app(self.app)
#         CORS(self.app)
#
#     # add routes
#     def add_routes(self):
#
#         self.app.add_url_rule('/', 'home', self.index, methods=['GET', 'POST'])
#
#     def index(self):
#         # Request the information from the user
#
#         ## request the list of shows from SQL and show in a drop down menu // automatic fill
#         with app.app_context():
#             result = db.session.execute(text("""
#                                  SELECT anime_id, name FROM anime WHERE rating > 8 and members > 200000
#                                  """)).fetchall()
#
#         test_list = dict(result)
#         tmp = test_list.values()
#         names = list(tmp)
#
#
#         ## output to HTML sheet
#
#         ##In the HTML
#         ## Select min 3 max 10 shows
#
#         ## Give ratings to these shows 0 - 10
#
#         ## input from HTML sheet
#         if request.method == "POST":
#              user_pref = [(1, 'Cowboy Bebop', 1.0), (19, 'Monster', 10.0), (33, 'Berserk', 7.0), (43, 'Ghost in the Shell', 9.5), (5114, 'Fullmetal Alchemist: Brotherhood', 10.0), (6702, 'Fairy Tail', 6.0), (18679, 'Kill la Kill', 6.5), (30276, 'One Punch Man', 7.0), (120, 'Fruits Basket', 10.0)]
#
#
#              ## These ratings, along with the user_id are fed back into the below function and recommendations for new shows are produced.
#              recommend_content = recommend_content(user_pref)
#
#
#              # !!!!! make the below into a function, potentially only one SQL command to increase speed.
#              first_rec = recommend_content[0]
#              second_rec = recommend_content[1]
#              third_rec = recommend_content[2]
#              with app.app_context():
#                  first = db.session.execute(text("SELECT name FROM anime WHERE anime_id = :first_rec"),
#                                         {"first_rec" : first_rec}).fetchone()
#
#                  second = db.session.execute(text("SELECT name FROM anime WHERE anime_id = :second_rec"),
#                                         {"second_rec" : second_rec}).fetchone()
#
#                  third = db.session.execute(text("SELECT name FROM anime WHERE anime_id = :third_rec"),
#                                         {"third_rec" : third_rec}).fetchone()
#
#              print(f"Recommended anime content for user: {first}, {second}, {third}")
#              return redirect(url_for("home"))
#         return render_template('home.html', names=names)
#
#     def start(self):
#         self.app.run(debug=True)
#
#
#
