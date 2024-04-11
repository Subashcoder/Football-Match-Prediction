import pickle
import streamlit as st
import pandas as pd
import numpy as np

# Function to load and merge data
def file_load():
    # File paths for CSV files
    url = r'C:\Drive D\Downloads\Lambton College\Semester 2\AI\Project\Football_Match_Prediction\Football-Match-Prediction\Data\data\2023-24\gws\gw28.csv'
    url2 = r'C:\Drive D\Downloads\Lambton College\Semester 2\AI\Project\Football_Match_Prediction\Football-Match-Prediction\Data\data\2023-24\player_idlist.csv'

    # Read the first CSV file (gw28.csv) to get player names and teams
    df_player = pd.read_csv(url)

    # Select only the 'name' and 'team' columns and remove duplicates
    df_player = df_player[['name', 'team']].drop_duplicates()

    # Read the second CSV file (player_idlist.csv) to get player names and IDs
    df_player_id = pd.read_csv(url2)

    # Create a 'name' column by concatenating 'first_name' and 'second_name'
    df_player_id['name'] = df_player_id['first_name'] + ' ' + df_player_id['second_name']

    # Select only the 'name' and 'id' columns and remove duplicates
    df_player_id = df_player_id[['name', 'id']].drop_duplicates()

    # Now df_player contains player names and teams from gw28.csv
    # And df_player_id contains player names and IDs from player_idlist.csv
    # Ensure 'name' columns are consistent for merging (convert to lowercase for case-insensitive matching)
    df_player['name'] = df_player['name'].str.lower()
    df_player_id['name'] = df_player_id['name'].str.lower()

    # Merge the two dataframes on 'name' to associate player IDs with player names and teams
    merged_df = pd.merge(df_player, df_player_id, on='name', how='inner')
    return merged_df

# Load merged data
merged_df = file_load()

def player_list(user_input):
        # Filter 'merged_df' based on the specified team name
        team_players = merged_df[merged_df['team'].str.lower() == user_input.lower()]
        
        # Check if team_players dataframe is not empty
        if not team_players.empty:
            # Extract player IDs for the specified team
            player_name = team_players['name'].tolist()
            players = pd.DataFrame({'Player Name': player_name})
            st.write(players)
        else:
            st.write("No players found for team '{}'.".format(player_name))

# Load the trained model using pickle
model_path = 'SVM_Model.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Function to generate random input data for prediction
def data_for_prediction():
    # Generate random input data with shape (1, 88)
    num_features = 88
    random_data = np.random.rand(1, num_features)
    return random_data

# Function to preprocess input data and make predictions
def predict(input_data):
    # Make predictions using the loaded model
    prediction = model.predict(input_data)
    return prediction

# Streamlit app function
import streamlit as st

import streamlit as st

import streamlit as st

def main():
    # Custom CSS style with background image
    css = """
    <style>
    body {
        background-image: url('fpl.png'); /* Replace with your image URL */
        background-size: cover; /* Cover the entire background */
        background-position: center; /* Center the background image */
        font-family: 'Roboto', sans-serif; /* Custom font (change 'Roboto' to desired font) */
        color: #333333; /* Dark text color */
        padding: 20px; /* Add padding for content */
    }
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #ffffff; /* White text color for the title */
        text-shadow: 2px 2px 5px rgba(255, 0, 0, 0.5); /* Text shadow effect */
        padding-top: 50px; /* Adjust padding for title positioning */
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)  # Apply custom CSS

    # Streamlit app title with custom styling
    st.markdown('<p class="title">Football Match Prediction</p>', unsafe_allow_html=True)

    # Display form inputs and prediction logic
    home_team = st.text_input('Enter Home Team', 'Enter here...', key='home_team_input')
    away_team = st.text_input('Enter Away Team', 'Enter here...', key='away_team_input')

    # Show starting 11 buttons side by side
    if st.button('Show Starting 11'):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Starting 11 for {home_team}")
            player_list(home_team)
        with col2:
            st.write(f"Starting 11 for {away_team}")
            player_list(away_team)

    # Prediction button
    if st.button('Predict'):
        # Placeholder for prediction logic
        result = predict(data_for_prediction())
        st.write('Prediction:', result)

# Run the app
if __name__ == '__main__':
    main()




