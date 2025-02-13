import pandas as pd
from sqlalchemy import create_engine
import os
from app import __init__, db, Anime, User

engine = create_engine('sqlite:///instance/anime.db')

# Load CSV file using pandas
anime_df = pd.read_csv('anime.csv')
user_df = pd.read_csv("rating_short.csv")

## Data clean

# None needed

# Handle missing values (replace NaN with default values)
with app.app_context():
    # Efficient bulk insert
    anime_df.to_sql('anime', con=engine, if_exists="append", index=False)
    user_df.to_sql('user', con=engine, if_exists="append", index=False)

    print("Data imported succesfully!")



