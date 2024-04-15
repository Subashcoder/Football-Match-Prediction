import pandas as pd
import json
import numpy as np
import requests
import time
import os
import streamlit as st

def file_load():
    '''Return the player_ID and team name table'''
    # File paths for CSV files
    dir = os.getcwd()
    url = r'Data\data\2023-24\gws\gw28.csv'
    url2 = r'Data\data\2023-24\player_idlist.csv'
    url3 = r'Data\data\2023-24\teams.csv'
    
    url_ = os.path.join(dir,url)
    # Player Name and Player Team
    df_player = pd.read_csv(url_)
    df_player = df_player[['name', 'team']].drop_duplicates()

    # Player name and palyer ID
    url2_ = os.path.join(dir, url2)
    df_player_id = pd.read_csv(url2_)
    df_player_id['name'] = df_player_id['first_name'] + ' ' + df_player_id['second_name']
    
    url3_ = os.path.join(dir, url3)
    df_team_id = pd.read_csv(url3_)
    df_team_id = df_team_id[['id', 'name']]

    # Select only the 'name' and 'id' columns and remove duplicates
    df_player_id = df_player_id[['name', 'id']].drop_duplicates()
    df_player['name'] = df_player['name'].str.lower()
    df_player_id['name'] = df_player_id['name'].str.lower()

    # Merge the two dataframes on 'name' to associate player IDs with player names and teams
    merged_df = pd.merge(df_player, df_player_id, on='name', how='inner')
    return merged_df,df_team_id


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

