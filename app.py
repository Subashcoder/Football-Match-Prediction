import pickle
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from input_collector import file_load
from input_collector import get_fixtures_data


# Load merged data
merged_df, _ = file_load()

# Get a list of unique team names
team_names = merged_df['team'].unique().tolist()

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
            st.write("No players found for team '{}'.".format(user_input))

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
def main():
    # Streamlit app title
    st.title('Football Match Prediction')

    # Streamlit app title with custom styling
    st.markdown('<p class="title">Football Match Prediction</p>', unsafe_allow_html=True)
    
    fixtures = st.text_input("Enter the next fixture number", "Enter here...")
    if st.button("Show fixtures"):
        fixture = get_fixtures_data(int(fixtures))
        st.write(fixture)
    # Load the background image
    image = Image.open(r'fpl.png')

    # Set the background image for the app
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{image_to_base64(image)}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display form inputs and prediction logic
    home_team = st.selectbox('Select Home Team', team_names)
    away_team = st.selectbox('Select Away Team', team_names)

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

# Function to convert an image to base64 string
def image_to_base64(image):
    import base64
    from io import BytesIO
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode('utf-8')

# Run the app
if __name__ == '__main__':
    main()
