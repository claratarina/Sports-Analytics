import requests
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import numpy as np

# Function to fetch match IDs for a given competition and season
def fetch_match_ids(competition_id, season_id):
    matches_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/{competition_id}/{season_id}.json'
    response = requests.get(matches_url)
    matches = response.json()
    return [match['match_id'] for match in matches]

# Function to fetch touch events (all relevant events) for a team across specified matches
def fetch_touch_events(team_name, match_ids):
    touch_events = []
    relevant_event_types = ["Ball Receipt*", "Pass", "Ball Recovery", "Dribble", "Dispossessed", "Duel", "Interception", "Pressure", "Clearance", "Carry", "Shot"]
    
    for match_id in match_ids:
        events_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json'
        response = requests.get(events_url)
        match_events = response.json()
        
        for event in match_events:
            if event['team']['name'] == team_name and event['type']['name'] in relevant_event_types:
                event_location = event['location']
                if event_location:
                    touch_events.append(event_location)
                    
    return touch_events

# Function to plot the heatmap for multiple teams
def plot_heatmaps_for_teams(teams, competition_id, season_id, vmax=None):
    # Fetch match IDs for the competition and season
    match_ids = fetch_match_ids(competition_id, season_id)
    
    # Create a pitch object for drawing
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    
    # Calculate the number of rows and columns for the grid layout
    num_teams = len(teams)
    cols = 2  # Number of columns
    rows = (num_teams + 1) // cols  # Number of rows

    # Create a figure with subplots
    fig, axes = plt.subplots(rows, cols, figsize=(15, 10 * rows))
    axes = axes.flatten()

    for idx, team_name in enumerate(teams):
        ax = axes[idx]
        pitch.draw(ax=ax)
        
        # Fetch touch events for the team
        touch_events = fetch_touch_events(team_name, match_ids)
        
        # Convert touch locations to numpy array for plotting
        locations = np.array(touch_events)
        
        if locations.size > 0:
            # Unpack x and y coordinates
            x_coords, y_coords = zip(*locations)
            
            # Calculate the number of events in each bin
            bin_statistic = pitch.bin_statistic(x_coords, y_coords, statistic='count', bins=(6, 5))
            
            # Plot the heatmap
            heatmap = pitch.heatmap(bin_statistic, ax=ax, edgecolors='black', cmap='Reds', alpha=0.7, vmax=vmax)
            
            # Add a color scale using matplotlib directly
            cbar = plt.colorbar(heatmap, ax=ax)
            cbar.set_label(f'Number of touches', fontsize=12)
        
        # Set title
        ax.set_title(f"{team_name} Touch Heat Map", fontsize=15)

    # Remove any unused subplots
    for i in range(len(teams), len(axes)):
        fig.delaxes(axes[i])

    plt.tight_layout()
    plt.show()

# Parameters
teams = ["Spain Women's", "Sweden Women's", "England Women's"]
competition_id = 72  # competition ID
season_id = 107  # season ID

# Plot heatmaps for the teams
plot_heatmaps_for_teams(teams, competition_id, season_id, vmax=1000)  # Adjust vmax as needed