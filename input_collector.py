import pandas as pd
import json
import numpy as np
import requests
import time
<<<<<<< HEAD
=======
import os
import streamlit as st
>>>>>>> c42ecf8ec5d9075d48504cf513de8116fc8c36f6

def file_load():
    '''Return the player_ID and team name table'''
    # File paths for CSV files
<<<<<<< HEAD
    url = r'C:\Drive D\Downloads\Lambton College\Semester 2\AI\Project\Football_Match_Prediction\Football-Match-Prediction\Data\data\2023-24\gws\gw28.csv'
    url2 = r'C:\Drive D\Downloads\Lambton College\Semester 2\AI\Project\Football_Match_Prediction\Football-Match-Prediction\Data\data\2023-24\player_idlist.csv'
    url3 = r'C:\Drive D\Downloads\Lambton College\Semester 2\AI\Project\Football_Match_Prediction\Football-Match-Prediction\Data\data\2023-24\teams.csv'
    # Player Name and Player Team
    df_player = pd.read_csv(url)
    df_player = df_player[['name', 'team']].drop_duplicates()

    # Player name and palyer ID
    df_player_id = pd.read_csv(url2)
    df_player_id['name'] = df_player_id['first_name'] + ' ' + df_player_id['second_name']
    
    df_team_id = pd.read_csv(url3)
=======
    dir = os.getcwd()
    url = r'Data/data/2023-24/gws/gw28.csv'
    url2 = r'Data\data\2023-24\player_idlist.csv'
    url3 = r'Data\data\2023-24\teams.csv'
    
    url_ = os.path.join(dir,url)
    # Player Name and Player Team
    df_player = pd.read_csv('gw28.csv')
    df_player = df_player[['name', 'team']].drop_duplicates()

    # Player name and palyer ID
    url2_ = os.path.join(dir, url2)
    df_player_id = pd.read_csv('player_idlist.csv')
    df_player_id['name'] = df_player_id['first_name'] + ' ' + df_player_id['second_name']
    
    url3_ = os.path.join(dir, url3)
    df_team_id = pd.read_csv('teams.csv')
>>>>>>> c42ecf8ec5d9075d48504cf513de8116fc8c36f6
    df_team_id = df_team_id[['id', 'name']]

    # Select only the 'name' and 'id' columns and remove duplicates
    df_player_id = df_player_id[['name', 'id']].drop_duplicates()
    df_player['name'] = df_player['name'].str.lower()
    df_player_id['name'] = df_player_id['name'].str.lower()

    # Merge the two dataframes on 'name' to associate player IDs with player names and teams
    merged_df = pd.merge(df_player, df_player_id, on='name', how='inner')
    return merged_df,df_team_id


<<<<<<< HEAD
def expected_goal_involvements(Previous):
    # Calculate expected goal involvements based on data from the previous rows
    sum_goals_scored = Previous['goals_scored'].sum()
    sum_target_missed = Previous['target_missed'].sum()
    sum_assist = Previous['assists'].sum()
    sum_big_chance = Previous['big_chances_created'].sum()
    sum_key_passes = Previous['key_passes'].sum()

    Creativity = Previous['creativity'].mean()
    influance = Previous['influence'].mean()
    
    if (sum_goals_scored + sum_goals_scored + sum_target_missed + sum_assist + sum_big_chance + sum_key_passes ).all() != 0:
        # Calculate expected goal involvements using aggregated data from previous rows
        return ((sum_goals_scored / (sum_goals_scored + sum_goals_scored + sum_target_missed + sum_assist + sum_big_chance + sum_key_passes )) * (Creativity / 100) * (influance/ 100)) / 3
    else:
        return ((sum_goals_scored ) * (Creativity / 100) * (influance/ 100)) / 3
    

     
def expected_goals(Previous):
    sum_goals = Previous['goals_scored'].sum()
    threat = Previous['threat'].mean()
    return (sum_goals * (threat / 100)) / 3
  
  
    
def expected_goals_conceded(Previous):
    
    sum_goal_conceded = Previous['goals_conceded'].sum()
    error_leading_to_goal = Previous['errors_leading_to_goal']
    sum_error_leading_to_goal_attempt = Previous['errors_leading_to_goal']
    
    if (error_leading_to_goal + sum_error_leading_to_goal_attempt).all() != 0:
        expected_goal_conceded = sum_goal_conceded / (error_leading_to_goal + sum_error_leading_to_goal_attempt)
        return expected_goal_conceded / 3
    else:
        return sum_goal_conceded / 3
    
    

def expected_assists(Previous):
    Sum_Assists = Previous['assists'].sum()
    Sum_Open_play_crosses = Previous['open_play_crosses'].sum()
    key_passes = Previous['key_passes'].sum()
    ea_index = Previous['ea_index'].mean()
    
    if (Sum_Open_play_crosses + key_passes).all() != 0:
    
        xA = (Sum_Assists / (Sum_Open_play_crosses + key_passes)) * (ea_index / 100)
        return xA / 3
    
    else:
        return (Sum_Assists * (ea_index / 100)) / 3
    



def get_individual_player_data(player_id):
    """ Retrieve the player-specific detailed data for last 3 games
=======
def expected_goal(data):
    goal = data['goals_scored'].sum()
    tread = data['threat'].mean()
    return (goal * (tread / 100)) / 3

def expected_goal_involvement(data):
    goal = data['goals_scored'].sum()
    assists = data['assists'].sum()
    creativity = data['creativity'].mean()
    influency = data['influence'].mean()
    
    
    if (goal + assists).all() != 0:
        return ((goal / (goal + assists)) * ((creativity / 100) * (influency / 100))) / 3
    else:
        return ((goal) * ((creativity / 100) * (influency / 100))) / 3

def expected_goal_conceded(data):
    goal_conceded = data['goals_conceded'].mean()
    return goal_conceded

def expected_assists(data):
    assists = data['assists'].sum()
    creativity = data['creativity'].mean()
    influency = data['influence'].mean()
    
    return (assists * (creativity / 100) * (influency / 100)) / 3
    


def get_individual_player_data(player_id):
    """ Retrieve the player-specific detailed data for last 4 games (excluding the most recent match)
>>>>>>> c42ecf8ec5d9075d48504cf513de8116fc8c36f6

    Args:
        player_id (int): ID of the player whose data is to be retrieved
    """
    base_url = "https://fantasy.premierleague.com/api/element-summary/"
    full_url = base_url + str(player_id) + "/"
    response = ''
    while response == '':
        try:
            response = requests.get(full_url)
        except:
            time.sleep(5)
    if response.status_code != 200:
        raise Exception("Response was code " + str(response.status_code))
    data = json.loads(response.text)
    data = pd.DataFrame(data['history'])
    data.sort_values(by='kickoff_time', ascending=False, inplace=True)
<<<<<<< HEAD
    return data.head(3)

def player_stats_calculator():
    ...
=======
    
    # Exclude the first row (most recent match) and take the next 3 rows
    data = data.iloc[1:4]  # Exclude first row, take next 3 rows
    numeric_columns = ['creativity', 'ict_index', 'influence','threat', 'goals_scored', 'assists', 'goals_conceded', 'expected_assists', 'expected_goal_involvements','expected_goals','minutes','expected_goals_conceded' ]
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
    return data

def player_stat_calculator(player_list):
    player_stats = []
    for player_id in player_list:
        player_data = get_individual_player_data(player_id)
        
        player_stats.append({
            
            'creativity': player_data['creativity'].mean(),
            'ict_index': player_data['ict_index'].mean(),
            'threat': player_data['threat'].mean(),
            'last_3_game_expected_assists': expected_assists(player_data),
            'last_3_game_expected_goals': expected_goal(player_data),
            'expected_assists': player_data['expected_assists'],
            'expected_goal_involvements': player_data['expected_goal_involvements'],
            'expected_goals': player_data['expected_goals']    
        })
    df = pd.DataFrame(player_stats)
    return df
>>>>>>> c42ecf8ec5d9075d48504cf513de8116fc8c36f6


def get_fixtures_data(event):
    """ Retrieve the fixtures data for the season
    """
    url = "https://fantasy.premierleague.com/api/fixtures/"
    response = ''
    while response == '':
        try:
            response = requests.get(url)
        except:
            time.sleep(5)
    if response.status_code != 200:
        raise Exception("Response was code " + str(response.status_code))
    data = json.loads(response.text)
    
    data = pd.DataFrame(data)
    _, df_id = file_load()
    data = data.loc[(data['event'] == event), ['kickoff_time', 'team_h', 'team_a']]
    id_to_name_map = dict(zip(df_id['id'], df_id['name']))

    # Use map to apply the mapping to team_a and create team_name column
    data['team_a_name'] = data['team_a'].map(id_to_name_map)
    data['team_h_name'] = data['team_h'].map(id_to_name_map)
    
    return data

<<<<<<< HEAD
def Home_team_stats():
    pass
=======


def player_list(user_input, merged_df):
    # Filter 'merged_df' based on the specified team name (case-insensitive)
    team_players = merged_df[merged_df['team'].str.lower() == user_input.lower()]
    
    # Check if team_players dataframe is not empty
    if not team_players.empty:
        # Extract player IDs and names for the specified team
        player_ids = team_players['id'].tolist()
        player_names = team_players['name'].tolist()
        
        # Initialize an empty list to store player data
        player_data_list = []
        
        # Iterate over each player ID and name
        for player_id, player_name in zip(player_ids, player_names):
            # Get fixtures data for the current player_id
            player_fixtures_data = get_individual_player_data(player_id)  # Assuming get_individual_player_data works as expected
            
            # Check if at least two rows of data are available (excluding the most recent match)
            if len(player_fixtures_data) >= 2:
                # Select the second row (index 1) from the fixtures data
                player_data = player_fixtures_data.iloc[1].copy()  # Make a copy to avoid modifying the original DataFrame
                
                # Add player ID and name to the player_data
                player_data['player_id'] = player_id
                player_data['player_name'] = player_name
                
                # Append the modified player_data to player_data_list
                player_data_list.append(player_data)
        
        # Combine all player data into a single DataFrame
        if player_data_list:
            players_df = pd.DataFrame(player_data_list)
            # Sort players_df by 'minutes' column in descending order
            players_df.sort_values(by='minutes', ascending=False, inplace=True)
            
            # Display the top 11 players' names using Streamlit
            top_11_players = players_df.head(11)['player_name'].tolist()
            # st.write(top_11_players)
            
            # Return the top 11 player IDs and names
            return players_df.head(11)[['player_id', 'player_name']]
        else:
            # st.write("No valid player data found.")
            return pd.DataFrame(columns=['player_id', 'player_name'])  # Return empty DataFrame if no valid player data found
    else:
        # st.write("No players found for team '{}'.".format(user_input))
        return pd.DataFrame(columns=['player_id', 'player_name'])  # Return empty DataFrame if no players found for the specified team

>>>>>>> c42ecf8ec5d9075d48504cf513de8116fc8c36f6
