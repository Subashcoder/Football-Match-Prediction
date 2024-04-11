import pandas as pd
import json
import numpy as np
import requests
import time

def file_load():
    '''Return the player_ID and team name table'''
    # File paths for CSV files
    url = r'C:\Drive D\Downloads\Lambton College\Semester 2\AI\Project\Football_Match_Prediction\Football-Match-Prediction\Data\data\2023-24\gws\gw28.csv'
    url2 = r'C:\Drive D\Downloads\Lambton College\Semester 2\AI\Project\Football_Match_Prediction\Football-Match-Prediction\Data\data\2023-24\player_idlist.csv'

    # Player Name and Player Team
    df_player = pd.read_csv(url)
    df_player = df_player[['name', 'team']].drop_duplicates()

    # Player name and palyer ID
    df_player_id = pd.read_csv(url2)
    df_player_id['name'] = df_player_id['first_name'] + ' ' + df_player_id['second_name']

    # Select only the 'name' and 'id' columns and remove duplicates
    df_player_id = df_player_id[['name', 'id']].drop_duplicates()
    df_player['name'] = df_player['name'].str.lower()
    df_player_id['name'] = df_player_id['name'].str.lower()

    # Merge the two dataframes on 'name' to associate player IDs with player names and teams
    merged_df = pd.merge(df_player, df_player_id, on='name', how='inner')
    return merged_df


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


def get_fixtures_data():
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
    return data