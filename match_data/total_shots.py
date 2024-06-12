import requests
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import numpy as np

def fetch_match_stats(team_name, match_id):
    events_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json'
    response = requests.get(events_url)
    match_events = response.json()
    
    shots = []
    shots_on_target = []
    goals = 0
    periods = set()

    for event in match_events:
        period = event['period']
        periods.add(period)
        if period > 4: 
            continue
        
        if event['team']['name'] == team_name:
            if event['type']['name'] == "Shot":
                location = event['location']
                if location:
                    shots.append(location)
                    if event['shot']['outcome']['name'] in ["Goal", "Saved"]:
                        shots_on_target.append(location)
                    if event['shot']['outcome']['name'] == "Goal":
                        goals += 1

    return shots, shots_on_target, goals, periods


def plot_match_stats_for_team(team_name, match_id):
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    fig, ax = plt.subplots(figsize=(10, 6))
    pitch.draw(ax=ax)
    
    
    shots, shots_on_target, goals, periods = fetch_match_stats(team_name, match_id)
    
    
    shot_locations = np.array(shots)
    shot_on_target_locations = np.array(shots_on_target)
    
    if shot_locations.size > 0:
        x_coords, y_coords = zip(*shot_locations)
        ax.scatter(x_coords, y_coords, c='blue', label='Shots', alpha=0.7)
    
    if shot_on_target_locations.size > 0:
        x_coords, y_coords = zip(*shot_on_target_locations)
        ax.scatter(x_coords, y_coords, c='red', label='Shots on Target', alpha=0.7)
    
   
    total_shots = len(shots)
    total_shots_on_target = len(shots_on_target)
    periods_played = len(periods)
    
    ax.text(0.5, 1.05, f"Total shots: {total_shots}", ha='center', va='center', transform=ax.transAxes, fontsize=12, color='black')
    ax.text(0.5, 1.1, f"Total shots on target: {total_shots_on_target}", ha='center', va='center', transform=ax.transAxes, fontsize=12, color='black')
    ax.text(0.5, 1.15, f"Total goals: {goals}", ha='center', va='center', transform=ax.transAxes, fontsize=12, color='black')
    ax.text(0.5, 1.2, f"Periods played: {periods_played}", ha='center', va='center', transform=ax.transAxes, fontsize=12, color='black')

    
    ax.set_title(f"{team_name} Match Stats (Match ID: {match_id})", fontsize=15)
    ax.legend()
    plt.tight_layout()
    plt.show()


team_name = "Germany Women's"
match_id = 3835322


plot_match_stats_for_team(team_name, match_id)
