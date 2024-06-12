import requests
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# Function to fetch match IDs for a given competition and season
def fetch_match_ids(competition_id, season_id):
    matches_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/{competition_id}/{season_id}.json'
    response = requests.get(matches_url)
    matches = response.json()
    return [match['match_id'] for match in matches]

# Function to fetch completed line breaks for selected teams across specified matches
def fetch_completed_line_breaks_for_selected_teams(selected_teams, match_ids):
    completed_line_breaks_by_match = {}

    for match_id in match_ids:
        events_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json'
        response = requests.get(events_url)
        match_events = response.json()

        last_defender_x = float('-inf')  # Initialize last defender's x position

        # Find the last player in the opposition team's defensive line
        for event in match_events:
            if event['team']['name'] not in selected_teams and event['type']['name'] == "Defensive":
                defender_position = event['location']
                if defender_position and defender_position[0] > last_defender_x:
                    last_defender_x = defender_position[0]

        completed_line_breaks = []  # List to store completed line breaks for this match

        # Iterate through pass events to check if they move beyond the last defender
        for event in match_events:
            if event['team']['name'] in selected_teams and event['type']['name'] == "Pass":
                pass_start_location = event['location']
                pass_end_location = event['pass'].get('end_location')

                if pass_start_location and pass_end_location:
                    pass_start_x, pass_start_y = pass_start_location
                    pass_end_x, pass_end_y = pass_end_location

                    # Check if the pass is significantly forward and into the opponent's half
                    if pass_end_x > pass_start_x and pass_end_x > 60:
                        # Check if the pass moves beyond the last defender
                        if last_defender_x is not None and pass_end_x > last_defender_x:
                            completed_line_breaks.append((pass_start_location, pass_end_location))

        completed_line_breaks_by_match[match_id] = completed_line_breaks

    return completed_line_breaks_by_match

# Function to plot completed line breaks for a given match
def plot_completed_line_breaks_for_match(match_id, completed_line_breaks):
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    fig, ax = plt.subplots(figsize=(10, 7))
    pitch.draw(ax=ax)
    
    for start_loc, end_loc in completed_line_breaks:
        start_x, start_y = start_loc
        end_x, end_y = end_loc
        ax.plot([start_x, end_x], [start_y, end_y], color='blue', alpha=0.7)
    
    ax.set_title(f"Completed Line Breaks - Match ID: {match_id}", fontsize=15)
    plt.show()

# Parameters
selected_team = "Sweden Women's"
competition_id = 72  # competition ID
season_id = 107  # season ID
selected_team_match_ids = [3893796, 3893814, 3893830, 3901797, 3902239, 3904628, 3906389]  # Match IDs for Sweden

# Fetch completed line breaks for the selected team's matches
completed_line_breaks_by_match = fetch_completed_line_breaks_for_selected_teams([selected_team], selected_team_match_ids)

# Plot completed line breaks for each match
for match_id, completed_line_breaks in completed_line_breaks_by_match.items():
    plot_completed_line_breaks_for_match(match_id, completed_line_breaks)
