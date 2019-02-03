import requests
import pandas as pd

api_url = "https://fantasy.premierleague.com/drf/bootstrap-static"
bootstrap_static_request = requests.get(api_url)
bootstrap_static_data = bootstrap_static_request.json()

# Short list of player positions.
positions = []
for i in bootstrap_static_data['element_types']:
    positions.append(i)

positions_df = pd.DataFrame(positions)
positions_df = positions_df[['id', 'plural_name_short']]

# Core dataset
elements_data = []

for i in bootstrap_static_data['elements']:
    elements_data.append(i)

elements_df = pd.DataFrame(elements_data)
elements_df['name'] = elements_df['first_name'] + " " + elements_df['second_name']

# Address a different end point using player ids
prev_gws = pd.DataFrame()
for i in elements_df['id']:
    print(i)
    request = requests.get(
        'https://fantasy.premierleague.com/drf/element-summary/' + str(i))
    data = request.json()
    gw_data = pd.DataFrame(data['history'])
    gw_data['player_id'] = i
    gw_data['round'] = gw_data['round'].astype(int)
    gw_data['next_week'] = (gw_data['round'] - 1)
    gw_data = gw_data.merge(gw_data,
                            left_on='round',
                            right_on='next_week',
                            how='inner')  # create an offset to self join.

    prev_gws = pd.concat([prev_gws, gw_data], ignore_index=True)

name_df = elements_df[['id', 'name', 'element_type', 'team']]
prev_gws = prev_gws.merge(name_df,
                          left_on='player_id_x',
                          right_on='id',
                          how='outer')
prev_gws = prev_gws.merge(positions_df,
                          left_on='element_type',
                          right_on='id',
                          how='outer')

prev_gws = prev_gws[['player_id_x', 'name', 'team', 'plural_name_short',
                     'assists_x', 'attempted_passes_x',
                     'big_chances_created_x', 'big_chances_missed_x',
                     'bps_x', 'clean_sheets_x',
                     'clearances_blocks_interceptions_x',
                     'completed_passes_x', 'creativity_x',
                     'dribbles_x', 'ea_index_x', 'errors_leading_to_goal_x',
                     'errors_leading_to_goal_attempt_x',
                     'goals_conceded_x', 'goals_scored_x', 'ict_index_x',
                     'influence_x', 'key_passes_x', 'loaned_in_x',
                     'loaned_out_x', 'minutes_x', 'open_play_crosses_x',
                     'opponent_team_x', 'own_goals_x', 'penalties_conceded_x',
                     'penalties_missed_x', 'penalties_saved_x', 'saves_x',
                     'tackles_x', 'target_missed_x', 'threat_x',
                     'winning_goals_x', 'fixture_y',
                     'value_x', 'total_points_y']]

api_url = "https://fantasy.premierleague.com/drf/fixtures/"
fixture_request = requests.get(api_url)
fixture_data = fixture_request.json()
fixtures_df = pd.DataFrame(fixture_data)
fixtures_df = fixtures_df[['id', 'event', 'finished', 'team_h',
                           'team_h_difficulty', 'team_a',
                           'team_a_difficulty']]
h_fixtures_df = fixtures_df[['id', 'team_h', 'team_a_difficulty']]
h_fixtures_df.rename(columns={'team_h': 'team',
                              'team_a_difficulty': 'difficulty'},
                     inplace=True)
a_fixtures_df = fixtures_df[['id', 'team_a', 'team_h_difficulty']]
a_fixtures_df.rename(columns={'team_a': 'team',
                              'team_h_difficulty': 'difficulty'},
                     inplace=True)
fix_df = pd.concat([h_fixtures_df, a_fixtures_df])
fix_df['index'] = fix_df['id'].astype(str) + '-' + fix_df['team'].astype(str)

prev_gws.fixture_y.fillna(0, inplace=True)
prev_gws['fixture_y'] = prev_gws['fixture_y'].astype('int64')

prev_gws['fixture_team_index'] = prev_gws['fixture_y'].astype(str) + "-" + prev_gws['team'].astype(str)

prev_gws = prev_gws.merge(fix_df,
                          left_on='fixture_team_index',
                          right_on='index',
                          how='inner')

prev_gws = prev_gws[['player_id_x', 'name', 'plural_name_short',
                     'assists_x', 'attempted_passes_x',
                     'big_chances_created_x', 'big_chances_missed_x',
                     'bps_x', 'clean_sheets_x',
                     'clearances_blocks_interceptions_x',
                     'completed_passes_x', 'creativity_x',
                     'dribbles_x', 'ea_index_x', 'errors_leading_to_goal_x',
                     'errors_leading_to_goal_attempt_x',
                     'goals_conceded_x', 'goals_scored_x', 'ict_index_x',
                     'influence_x', 'key_passes_x', 'loaned_in_x',
                     'loaned_out_x', 'minutes_x', 'open_play_crosses_x',
                     'opponent_team_x', 'own_goals_x', 'penalties_conceded_x',
                     'penalties_missed_x', 'penalties_saved_x', 'saves_x',
                     'tackles_x', 'target_missed_x', 'threat_x',
                     'winning_goals_x',
                     'value_x', 'difficulty', 'total_points_y']]

file_name = "fpl_data.csv"
prev_gws.to_csv(file_name)