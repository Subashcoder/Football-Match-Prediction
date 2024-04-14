<<<<<<< HEAD
from IPython.display import display, HTML

# HTML and CSS code for the UI
html_code = '''
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-image: url('football.jpg'); /* Replace 'football_background.jpg' with your image path */
            background-size: cover;
            font-family: Arial, sans-serif;
            color: white;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
            padding: 20px;
            border-radius: 10px;
        }
        h1 {
            text-align: center;
            font-size: 36px;
            margin-bottom: 20px;
        }
        .input-field {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: none;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.8); /* Semi-transparent background */
            color: #333;
            outline: none;
        }
        .btn {
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 5px;
            background: #007bff; /* Blue color */
            color: white;
            cursor: pointer;
            outline: none;
        }
        .btn:hover {
            background: #0056b3; /* Darker blue color on hover */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Football Match Prediction</h1>
        <form>
            <input type="text" class="input-field" placeholder="Enter Team A">
            <input type="text" class="input-field" placeholder="Enter Team B">
            <button type="submit" class="btn">Predict</button>
        </form>
    </div>
</body>
</html>
'''

# Display the HTML code
display(HTML(html_code))
=======
import pickle
import streamlit as st
import pandas as pd
import numpy as np
<<<<<<< HEAD
from input_collector import file_load
from input_collector import get_fixtures_data

# Loading function to export player list file_load() return the merge_df which have player ID corresponding to team
merged_df, _ = file_load()
=======
from PIL import Image

# Function to load and merge data
def file_load():
    # File paths for CSV files
    url = r'C:\Users\Keshav Gautam\Desktop\AI_Project\Football-Match-Prediction\data\data\2023-24\gws\gw28.csv'
    url2 = r'C:\Users\Keshav Gautam\Desktop\AI_Project\Football-Match-Prediction\data\data\2023-24\player_idlist.csv'

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
>>>>>>> 2dcf081a7aae290117dc53c6fe30f8b15537a3a6

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

<<<<<<< HEAD
=======
# Streamlit app function
>>>>>>> 2dcf081a7aae290117dc53c6fe30f8b15537a3a6
def main():
    # Streamlit app title
    st.title('Football Match Prediction')

<<<<<<< HEAD
    # Streamlit app title with custom styling
    st.markdown('<p class="title">Football Match Prediction</p>', unsafe_allow_html=True)
    
    fixtures = st.text_input("Enter the next fixture number", "Enter here...")
    if st.button("Show fixtures"):
        fixture = get_fixtures_data(int(fixtures))
        st.write(fixture)
=======
    # Load the background image
    image = Image.open(r'C:\Users\Keshav Gautam\Desktop\AI_Project\ftl.png')

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
>>>>>>> 2dcf081a7aae290117dc53c6fe30f8b15537a3a6

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
>>>>>>> 4601a74502a69f048142d2be7bfdf8872a54a96c
