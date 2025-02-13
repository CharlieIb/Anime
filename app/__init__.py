# Flask and SQL
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
# DB
from app.Archive.database import db
# Recommendation process
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

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



class FrontEndConnector:
    db = SQLAlchemy()

    def __init__(self):
        # Initialise the app
        self.app = Flask(__name__)

        # Connect to the DB
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///anime.db"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Initialise the database with the app
        self.db.init_app(self.app)
        CORS(self.app)

        # Add routes
        self.add_routes()


    def add_routes(self):
        self.app.add_url_rule('/', 'home', self.home, methods=['GET', 'POST'])


    # Routes
    def home(self):
        print("index called")
        if request.method == "POST":
            # Process user input
            user_pref = self.input_pref()

            ## These ratings, along with the user_id are fed back into the below function and recommendations for new shows are produced.
            recommended_content = self.recommend_content(user_pref)

            # Get the names from the recommended content
            recommended_names = self.get_recommended_names(recommended_content)

            # Printing to check
            print(f"Recommended anime content for user: {recommended_names[0]}, {recommended_names[1]},{recommended_names[2]}")
            return render_template("home.html", names=self.get_anime_names(), recommendations=recommended_names)
        return render_template('home.html', names=self.get_anime_names(), recommendations=None)



    # Helper methods
    def get_anime_names(self):
        print("get anime called")
        # Fetch sample anime names from the database. These names should be ones commonly recognised
        with self.app.app_context():
            result = self.db.session.execute(text("""
            SELECT anime_id, name FROM anime WHERE rating > 8.0 AND members > 200000
            """)).fetchall()

        # Extract the names from the result
        names = [row[1] for row in result]
        return names

    def input_pref(self):
        user_pref = [(1, 'Cowboy Bebop', 1.0), (19, 'Monster', 10.0), (33, 'Berserk', 7.0),
                     (43, 'Ghost in the Shell', 9.5), (5114, 'Fullmetal Alchemist: Brotherhood', 10.0),
                     (6702, 'Fairy Tail', 6.0), (18679, 'Kill la Kill', 6.5), (30276, 'One Punch Man', 7.0),
                     (120, 'Fruits Basket', 10.0)]
        return user_pref

    def recommend_content(self, new_user_data, top_n=3):

        query = "SELECT anime.anime_id, user_id, user.rating FROM anime JOIN user ON anime.anime_id = user.anime_id WHERE user.rating > 0;"
        with self.app.app_context():
            df = pd.read_sql(query, con=self.db.engine)

        # New user requires a user id - here we max the ids in the current df and add 1
        new_user_id = df['user_id'].max() + 1 if not df.empty else 1

        # New user input data from app (Format: List of Tuples: anime_id, name, rating)
        new_user_df = pd.DataFrame(
            {
                'anime_id': [anime_id for anime_id, _, _ in new_user_data],
                'user_id': [new_user_id] * len(new_user_data),
                'rating': [rating for _, _, rating in new_user_data]
            }
        )

        # Add the new user data to the dataframe
        df = pd.concat([df, new_user_df], ignore_index=True)

        print("\n Successfully updated DataFrame with user input data")

        # Create the user-content interaction matrix
        user_inter_matrix = df.pivot(index="user_id", columns="anime_id", values="rating").fillna(0)

        # Convert to a spare matrix format
        user_inter_matrix_sparse = csr_matrix(user_inter_matrix.values)

        # Calculate the similarity between pairs of users
        cosine_sim = cosine_similarity(user_inter_matrix_sparse)

        # Convert the result to a dataframe for readability
        cosine_sim_df = pd.DataFrame(cosine_sim, index=user_inter_matrix.index, columns=user_inter_matrix.index)

        similar_users = cosine_sim_df[new_user_id].sort_values(ascending=False)
        recommended_content = set()  # Avoid duplicates

        # Get the movies already rated by the target user
        target_user_ratings = user_inter_matrix.loc[new_user_id]
        watched_movies = target_user_ratings[target_user_ratings > 0].index

        for similar_user, similarity in similar_users.items():

            # Get the movies rated by the similar user
            similar_user_ratings = user_inter_matrix.loc[similar_user]
            # Find movies that the similar user has rated but the target user has not
            new_recommendations = similar_user_ratings[
                (similar_user_ratings > 0) & (~similar_user_ratings.index.isin(watched_movies))].index

            recommended_content.update(new_recommendations)

            if len(recommended_content) >= top_n:
                break

        return list(recommended_content)[:top_n]

    def get_recommended_names(self, recommended_content):


        with self.app.app_context():

            # Dynamically generate placeholders
            placeholders = ', '.join([':id{}'.format(i) for i in range(len(recommended_content))])

            # Query for SQL
            query = text(f"""
                    SELECT name 
                    FROM anime
                    WHERE anime_id IN ({placeholders})
                """)

            # Dynamically create a dictionary of parameters for the query
            params = {f'id{i}': anime_id for i, anime_id in enumerate(recommended_content)}

            # Execute the query with the parameters
            result = self.db.session.execute(query, params).fetchall()

        # Unpack the names from the result
        names = [row[0] for row in result]
        return names



    def start(self):
        self.app.run(debug=True)






if __name__ == "__main__":
    print("Entering main")
    my_app = FrontEndConnector()
    my_app.start()