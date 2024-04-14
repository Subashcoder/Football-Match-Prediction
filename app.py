import pickle
import streamlit as st
import pandas as pd
import numpy as np
from input_collector import file_load
from input_collector import get_fixtures_data

# Loading function to export player list file_load() return the merge_df which have player ID corresponding to team
merged_df, _ = file_load()

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
    
    fixtures = st.text_input("Enter the next fixture number", "Enter here...")
    if st.button("Show fixtures"):
        fixture = get_fixtures_data(int(fixtures))
        st.write(fixture)

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




