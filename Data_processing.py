import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from database import db

engine = create_engine('sqlite:///instance/anime.db')


# Process the data
def recommend_content(user_id, top_n=3):

    query = "SELECT anime.anime_id, user_id, user.rating FROM anime JOIN user ON anime.anime_id = user.anime_id WHERE user.rating > 0;"
    df = pd.read_sql(query, con=engine)

    # Create the user-content interaction matrix
    user_inter_matrix = df.pivot(index="user_id", columns="anime_id", values="rating").fillna(0)

    # Convert to a spare matrix format
    user_inter_matrix_sparse = csr_matrix(user_inter_matrix.values)

    # Calculate the similarity between pairs of users
    cosine_sim = cosine_similarity(user_inter_matrix_sparse)

    # Convert the result to a dataframe for readability
    cosine_sim_df = pd.DataFrame(cosine_sim, index=user_inter_matrix.index, columns=user_inter_matrix.index)

    similar_users = cosine_sim_df[user_id].sort_values(ascending=False)
    recommended_content = set() # Avoid duplicates

    # Get the movies already rated by the target user
    target_user_ratings = user_inter_matrix.loc[user_id]
    watched_movies = target_user_ratings[target_user_ratings > 0].index

    for similar_user, similarity in similar_users.items():

        # Get the movies rated by the similar user
        similar_user_ratings = user_inter_matrix.loc[similar_user]
        # Find movies that the similar user has rated but the target user has not
        new_recommendations = similar_user_ratings[(similar_user_ratings > 0) & (~similar_user_ratings.index.isin(watched_movies))].index

        recommended_content.update(new_recommendations)


        if len(recommended_content) >= top_n:
            break

    return list(recommended_content)[:top_n]
