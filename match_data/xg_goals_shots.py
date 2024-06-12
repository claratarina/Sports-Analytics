import requests
import matplotlib.pyplot as plt
from mplsoccer import Pitch

def plot_goal_shot_locations(match_events, match_id):
    sweeden_events = [event for event in match_events if event['team']['name'] == "Sweden Women's" and event['period'] in range(1, 5)]

    shot_events = [event for event in sweeden_events if 'shot' in event]

    fig, ax = plt.figure(figsize=(10, 7)), plt.gca()
    pitch = Pitch(pitch_type='statsbomb')
    pitch.draw(ax=ax)
    
    goal_players = []
    total_goals = 0
    total_xG = 0.0
    home_team_name = match_events[0]['team']['name']
    away_team_name = match_events[1]['team']['name']
    
    for event in shot_events:
        xG = event['shot'].get('statsbomb_xg', 0)  
        total_xG += xG
        shot_type_name = event['shot']['type']['name'] if 'type' in event['shot'] else 'Unknown'
        if 'outcome' in event['shot'] and event['shot']['outcome']['name'] == 'Goal':
            total_goals += 1
            player_name = event['player']['name']
            goal_players.append((player_name, xG, shot_type_name))
           
            ax.plot(event['location'][0], event['location'][1], 'ro', markersize=10)
            ax.annotate(f"{xG:.2f}, {shot_type_name}", (event['location'][0], event['location'][1]), 
                        textcoords="offset points", xytext=(0,10), ha='center', color='black', fontsize=7, fontweight='regular')
        else:
            
            ax.plot(event['location'][0], event['location'][1], 'bo', markersize=5)
            ax.annotate(f"{xG:.2f}", (event['location'][0], event['location'][1]), 
                        textcoords="offset points", xytext=(0,5), ha='center', color='grey', fontsize=7, fontweight='regular')
    
    player_info_str = '\n'.join([f"{name}: xG {xG:.2f}, Shot type: {shot_type}" for name, xG, shot_type in goal_players])
    ax.text(0.5, -0.05, f"Goals with xG and shot type:\n{player_info_str}", 
            horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=10)
    
    match_info_str = f"Match ID: {match_id}, Home Team: {home_team_name}, Away Team: {away_team_name}"
    summary_str = f"Total Goals: {total_goals}, ∑(xG for total shots): {total_xG:.2f}"
    ax.set_title(f"{match_info_str}\n{summary_str}", fontsize=12)

match_ids = [3893796, 3893830, 3902239, 3901797, 3893814, 3904628, 3906389]  

for match_id in match_ids:
    
    events_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json'
    response = requests.get(events_url)
    match_events = response.json()
    
    
    plot_goal_shot_locations(match_events, match_id)

plt.show()
