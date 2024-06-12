import requests
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import numpy as np
from matplotlib.colors import Normalize

def fetch_events_for_match(team_name, match_id):
    recoveries = []
    interceptions = []
    events_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json'
    response = requests.get(events_url)
    match_events = response.json()
    
    for event in match_events:
        if event['team']['name'] == team_name:
            if event['type']['name'] == "Ball Recovery":
                offensive = event.get('ball_recovery', {}).get('offensive', True)
                location = event.get('location')
                if location and location[0] > 60 and offensive: 
                    recoveries.append(location)
            elif event['type']['name'] == "Interception":
                outcome = event.get('interception', {}).get('outcome', {}).get('name')
                if outcome in {"Success", "Success In Play", "Success Out", "Won"}:
                    location = event.get('location')
                    if location and location[0] > 60:  
                        interceptions.append(location)
                
    return recoveries, interceptions

def plot_events_for_team(team_name, match_ids):
    all_recoveries = []
    all_interceptions = []
    valid_events = []
    
    for match_id in match_ids:
        recoveries, interceptions = fetch_events_for_match(team_name, match_id)
        if recoveries or interceptions:
            valid_events.append((match_id, recoveries, interceptions))
            all_recoveries.extend(recoveries)
            all_interceptions.extend(interceptions)
    
    num_matches = len(valid_events)
    cols = 3
    rows = (num_matches + cols - 1) // cols  
    
    fig, axes = plt.subplots(rows + 1, cols, figsize=(16, 8 * (rows + 1)))  
    axes = axes.flatten()
    
    for i, (match_id, ball_recoveries, interceptions) in enumerate(valid_events):
        ax = axes[i]
        pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
        pitch.draw(ax=ax)
        
        all_events = ball_recoveries + interceptions
        
        if all_events:
            locations = np.array(all_events)
            
            if locations.size > 0:
                x_coords, y_coords = zip(*locations)
                
                bin_statistic = pitch.bin_statistic(x_coords, y_coords, statistic='count', bins=(12, 10))
                
                max_bin_count = bin_statistic['statistic'].max()
                norm = Normalize(vmin=0, vmax=max_bin_count)
                cmap = plt.cm.Purples
                
                pc = pitch.heatmap(bin_statistic, ax=ax, cmap=cmap, edgecolors='black', alpha=0.7)
                
                for k in range(bin_statistic['statistic'].shape[0]):
                    for j in range(bin_statistic['statistic'].shape[1]):
                        bin_count = bin_statistic['statistic'][k, j]
                        bin_center = bin_statistic['cx'][k, j], bin_statistic['cy'][k, j]
                        ax.text(bin_center[0], bin_center[1], str(int(bin_count)),
                                ha='center', va='center', fontsize=10, color='black')
            
            total_recoveries = len(ball_recoveries)
            total_interceptions = len(interceptions)
            total_events = total_recoveries + total_interceptions
            ax.text(0.5, 1.15, f"Total recoveries: {total_recoveries}, Total interceptions: {total_interceptions}, Total events: {total_events}",
                    ha='center', va='center', transform=ax.transAxes, fontsize=10, color='black')
            
            ax.set_title(f"{team_name} Events Map for Match {match_id}, WC 2023", fontsize=10)
    
    for j in range(len(valid_events), len(axes) - 1):  
        fig.delaxes(axes[j])
    
    ax_combined = axes[-1]
    pitch_combined = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    pitch_combined.draw(ax=ax_combined)
    
    all_events_combined = all_recoveries + all_interceptions
    
    if all_events_combined:
        locations_combined = np.array(all_events_combined)
        
        if locations_combined.size > 0:
            x_coords_combined, y_coords_combined = zip(*locations_combined)
            
            bin_statistic_combined = pitch_combined.bin_statistic(x_coords_combined, y_coords_combined, statistic='count', bins=(12, 10))
            
            max_bin_count_combined = bin_statistic_combined['statistic'].max()
            norm_combined = Normalize(vmin=0, vmax=max_bin_count_combined)
            cmap_combined = plt.cm.Purples
            
            pc_combined = pitch_combined.heatmap(bin_statistic_combined, ax=ax_combined, cmap=cmap_combined, edgecolors='black', alpha=0.7)
            
            for k in range(bin_statistic_combined['statistic'].shape[0]):
                for j in range(bin_statistic_combined['statistic'].shape[1]):
                    bin_count_combined = bin_statistic_combined['statistic'][k, j]
                    bin_center_combined = bin_statistic_combined['cx'][k, j], bin_statistic_combined['cy'][k, j]
                    ax_combined.text(bin_center_combined[0], bin_center_combined[1], str(int(bin_count_combined)),
                                     ha='center', va='center', fontsize=10, color='black')
        
        total_recoveries_combined = len(all_recoveries)
        total_interceptions_combined = len(all_interceptions)
        total_events_combined = total_recoveries_combined + total_interceptions_combined
        ax_combined.text(0.5, 1.15, f"Total recoveries: {total_recoveries_combined}, Total interceptions: {total_interceptions_combined}, Total events: {total_events_combined}",
                         ha='center', va='center', transform=ax_combined.transAxes, fontsize=12, color='black')
        ax_combined.set_title(f"Combined Events Heatmap for {team_name}, WC 2023", fontsize=12)
    
    plt.tight_layout()
    plt.show()



# Parameters
team_name = "Germany Women's"
match_ids = [3847567, 3845507, 3844385, 3835338, 3835330, 3835322
]

plot_events_for_team(team_name, match_ids)
