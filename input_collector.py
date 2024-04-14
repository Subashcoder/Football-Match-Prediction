import pandas as pd
import json
import numpy as np
import requests
import time
import os

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
    return data.head(3)

def player_stats_calculator():
    ...


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

def Home_team_stats():
    pass