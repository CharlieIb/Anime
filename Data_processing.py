import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from database import db

engine = create_engine('sqlite:///instance/anime.db')


# Process the data
def recommend_content(new_user_data, top_n=3):

    query = "SELECT anime.anime_id, user_id, user.rating FROM anime JOIN user ON anime.anime_id = user.anime_id WHERE user.rating > 0;"
    df = pd.read_sql(query, con=engine)

    # New user requires a user id - here we max the ids in the current df and add 1
    new_user_id = df['user_id'].max() + 1 if not df.empty else 1

    # New user input data from app.py (Format: List of Tuples: anime_id, name, rating)
    new_user_df = pd.DataFrame(
        {
            'anime_id': [anime_id for anime_id, _, _ in new_user_data],
            'user_id' : [new_user_id] * len(new_user_data),
            'rating' : [rating for _, _, rating in new_user_data]
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
    recommended_content = set() # Avoid duplicates

    # Get the movies already rated by the target user
    target_user_ratings = user_inter_matrix.loc[new_user_id]
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
