import requests
import matplotlib.pyplot as plt
from mplsoccer import Pitch

def fetch_shot_events(team_name, match_id):
    events_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json'
    response = requests.get(events_url)
    match_events = response.json()
    shot_events = [event for event in match_events if event['team']['name'] == team_name and event['period'] in range(1, 5) and 'shot' in event]
    return shot_events

def plot_goal_shot_locations(team_name, match_id, shot_events):
    fig, ax = plt.subplots(figsize=(10, 7))
    pitch = Pitch(pitch_type='statsbomb')
    pitch.draw(ax=ax)
    
    goal_players = []
    total_goals = 0
    total_xG = 0
    
    for event in shot_events:
        xG = event['shot'].get('statsbomb_xg', 0)
        total_xG += xG
        shot_type_name = event['shot'].get('type', {}).get('name', 'Unknown')
        if event['shot'].get('outcome', {}).get('name') == 'Goal':
            total_goals += 1
            player_name = event['player']['name']
            goal_players.append((player_name, xG, shot_type_name))
            ax.plot(event['location'][0], event['location'][1], 'ro', markersize=10)
            ax.annotate(f"{xG:.2f}, {shot_type_name}", (event['location'][0], event['location'][1]), 
                        textcoords="offset points", xytext=(0,10), ha='center', color='black', fontsize=7)
        else:
            ax.plot(event['location'][0], event['location'][1], 'bo', markersize=5)
            ax.annotate(f"{xG:.2f}", (event['location'][0], event['location'][1]), 
                        textcoords="offset points", xytext=(0,5), ha='center', color='grey', fontsize=7)
    
    player_info_str = '\n'.join([f"{name}: xG {xG:.2f}, Shot type: {shot_type}" for name, xG, shot_type in goal_players])
    ax.text(1, 1, f"Goals with xG and shot type:\n{player_info_str}", 
            horizontalalignment='left', verticalalignment='center', transform=ax.transAxes, fontsize=6)
    
    total_shots = len(shot_events)
    summary_str = f"Total Goals: {total_goals}, Total Shots: {total_shots}, ∑(xG for total shots): {total_xG:.2f}"
    ax.set_title(f"{team_name} Match {match_id} Summary\n{summary_str}", fontsize=12)

# Parameters
team_name = "Germany Women's"
match_id = 3835322   

shot_events = fetch_shot_events(team_name, match_id)

plot_goal_shot_locations(team_name, match_id, shot_events)
plt.show()
