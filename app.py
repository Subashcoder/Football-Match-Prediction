<<<<<<< HEAD
import pickle
=======
>>>>>>> c42ecf8ec5d9075d48504cf513de8116fc8c36f6
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
<<<<<<< HEAD
from input_collector import file_load
from input_collector import get_fixtures_data

=======
import pickle
from input_collector import file_load, get_fixtures_data, player_list, player_stat_calculator
>>>>>>> c42ecf8ec5d9075d48504cf513de8116fc8c36f6

# Load merged data
merged_df, _ = file_load()

# Get a list of unique team names
team_names = merged_df['team'].unique().tolist()

<<<<<<< HEAD
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
=======
# Load the trained model using pickle
model_path = 'RandomForest.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Load the scaler using pickle
scaler_path = 'scaler.pkl'
with open(scaler_path, 'rb') as file:
    scaler = pickle.load(file)

# Function to preprocess input data and make predictions
def data_for_prediction(player_list):
    # Calculate player statistics for the specified team
    player_stats = player_stat_calculator(player_list)
    print(player_stats)
    
    # Ensure all columns contain numeric values without nested structures
    for col in player_stats.columns:
        player_stats[col] = player_stats[col].apply(lambda x: x if np.isscalar(x) else x.iloc[0])
    
    # Convert DataFrame to numpy array
    player_stats_array = player_stats.values
    
    # Reshape the array to (1, 11, 8)
    player_stats_array = player_stats_array.reshape(1, 11, 8)
    
    # Flatten the array to (1, 88)
    player_stats_array_flat = player_stats_array.flatten().reshape(1, -1)
    
    # Check the shape of the flattened array
    print("Shape of player_stats_array:", player_stats_array_flat.shape)
    
    return player_stats_array_flat




# Function to make predictions
def predict(input_data):
    # Make predictions using the loaded model
    prediction = model.predict(input_data)
    prediction_score = model.predict_proba(input_data)
    return prediction, prediction_score
>>>>>>> c42ecf8ec5d9075d48504cf513de8116fc8c36f6

# Streamlit app function
def main():
    # Streamlit app title
    st.title('Football Match Prediction')

    # Streamlit app title with custom styling
    st.markdown('<p class="title">Football Match Prediction</p>', unsafe_allow_html=True)
    
<<<<<<< HEAD
    fixtures = st.text_input("Enter the next fixture number", "Enter here...")
    if st.button("Show fixtures"):
        fixture = get_fixtures_data(int(fixtures))
        st.write(fixture)
    # Load the background image
    image = Image.open(r'fpl.png')
=======
    fixtures = st.text_input("Enter the next fixture number")
    

    # Load the background image
    image = Image.open('fpl2.jpg')
>>>>>>> c42ecf8ec5d9075d48504cf513de8116fc8c36f6

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
<<<<<<< HEAD
=======
    
    if fixtures:
        fixture = get_fixtures_data(int(fixtures))
        st.write(fixture)
        
        
>>>>>>> c42ecf8ec5d9075d48504cf513de8116fc8c36f6

    # Display form inputs and prediction logic
    home_team = st.selectbox('Select Home Team', team_names)
    away_team = st.selectbox('Select Away Team', team_names)

    # Show starting 11 buttons side by side
    if st.button('Show Starting 11'):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Starting 11 for {home_team}")
<<<<<<< HEAD
            player_list(home_team)
        with col2:
            st.write(f"Starting 11 for {away_team}")
            player_list(away_team)

    # Prediction button
    if st.button('Predict'):
        # Placeholder for prediction logic
        result = predict(data_for_prediction())
        st.write('Prediction:', result)
=======
            st.write(player_list(home_team, merged_df))
        with col2:
            st.write(f"Starting 11 for {away_team}")
            st.write(player_list(away_team, merged_df))

    # Prediction button
    if st.button('Predict'):
        player_id_list_home = player_list(home_team, merged_df)
        player_id_list = player_id_list_home['player_id'].tolist()
        
        # Placeholder for prediction logic
        input_data = data_for_prediction(player_id_list)
        result,prob = predict(input_data)
        
        # st.write('Prediction:', result)
        st.write("Prob", prob)
        st.write('Win probability:', f"{prob[0,0]:.2f}")
        st.write('Draw probability:', f"{prob[0, 1]:.2f}")
        st.write('Loss probability:', f"{prob[0, 2]:.2f}")
>>>>>>> c42ecf8ec5d9075d48504cf513de8116fc8c36f6

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
