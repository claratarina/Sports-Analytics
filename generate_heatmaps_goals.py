import requests 
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import numpy as np
from matplotlib.colors import ListedColormap

# Define a custom colormap with distinct colors for steps of 1
colors = ['#FFFFFF', '#FFCCCC', '#FF9999', '#FF6666', '#FF3333', '#FF0000']
custom_cmap = ListedColormap(colors)

# Function to collect a team's events during specified matches
def collect_team_events(team_name, match_ids, event_type, outcome=None):
    all_event_locations = []

    for match_id in match_ids:
        events_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json'
        response = requests.get(events_url)
        match_events = response.json()

        for event in match_events:
            if event['team']['name'] == team_name and event['type']['name'] == event_type:
                if outcome is None or (outcome is not None and event['shot']['outcome']['name'] == outcome):
                    event_location = event['location']
                    all_event_locations.append(event_location)

    return all_event_locations

# Plotting the heatmap
def plot_heatmap(all_event_locations, event_type, title):
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 7))

    # Create a pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')

    # Draw the pitch with sidelines and other markings
    pitch.draw(ax=ax)

    # Unpack x and y coordinates
    x_coords, y_coords = zip(*all_event_locations)

    # Calculate the number of events in each bin
    bin_statistic = pitch.bin_statistic(x_coords, y_coords, statistic='count', bins=(6, 5))

    # Plot the heatmap with opacity set to 0.7 and using the custom colormap
    heatmap = pitch.heatmap(bin_statistic, ax=ax, edgecolors='black', cmap=custom_cmap, alpha=0.7)

    # Add a color scale using matplotlib directly
    cbar = plt.colorbar(heatmap, ax=ax)
    cbar.set_label(f'Number of {event_type}', fontsize=12)

    # Set title
    ax.set_title(title, fontsize=15)

    plt.show()

if __name__ == "__main__":
    team_name = "Australia Women's"
    match_ids = [3904629, 3906389, 3902968, 3901736, 3893809, 3893788, 3893821]
    event_type = 'Shot'
    outcome = 'Goal'

    # Collect team's goals during the specified matches
    all_event_locations = collect_team_events(team_name, match_ids, event_type, outcome)

    # Plot the goals heatmap
    title = f"Heatmap of {team_name}'s {outcome}s during the tournament"
    plot_heatmap(all_event_locations, event_type, title)
