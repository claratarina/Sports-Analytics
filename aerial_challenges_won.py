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
    if response.status_code == 200:
        matches = response.json()
        return [match['match_id'] for match in matches]
    else:
        print(f"Failed to fetch match IDs: {response.status_code}")
        return []

# Function to fetch aerial challenges lost for a given team
def fetch_aerial_challenges_lost(team_name, match_ids):
    team_aerial_challenges_lost = []
    total_aerial_challenges_lost_in_matches = 0
    total_team_aerial_challenges_lost = 0

    for match_id in match_ids:
        events_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json'
        response = requests.get(events_url)
        if response.status_code == 200:
            match_events = response.json()
            match_teams = {event['team']['name'] for event in match_events if event['type']['name'] == "Duel"}
            if team_name in match_teams:
                for event in match_events:
                    if event['type']['name'] == "Duel" and event['duel']['type']['name'] == "Aerial Lost":
                        total_aerial_challenges_lost_in_matches += 1
                        if event['team']['name'] == team_name:
                            total_team_aerial_challenges_lost += 1
                            location = event.get('location')
                            if location:
                                team_aerial_challenges_lost.append(location)
        else:
            print(f"Failed to fetch events for match ID {match_id}: {response.status_code}")

    return team_aerial_challenges_lost, total_aerial_challenges_lost_in_matches, total_team_aerial_challenges_lost

# Function to plot the aerial challenges lost for a team in the tournament
def plot_aerial_challenges_lost_for_team_in_tournament(team_name, competition_id, season_id):
    # Fetch match IDs for the competition and season
    match_ids = fetch_match_ids(competition_id, season_id)
    
    if not match_ids:
        print("No match IDs found, exiting.")
        return
    
    fig, ax = plt.subplots(figsize=(10, 7))
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    pitch.draw(ax=ax)

    # Fetch aerial challenges lost for the team
    team_aerial_challenges_lost, total_aerial_challenges_lost_in_matches, total_team_aerial_challenges_lost = fetch_aerial_challenges_lost(team_name, match_ids)
    
    # Convert challenge locations to numpy array for plotting
    locations = np.array(team_aerial_challenges_lost)
    
    if locations.size > 0:
        # Unpack x and y coordinates
        x_coords, y_coords = zip(*locations)
        
        # Calculate the number of events in each bin
        bin_statistic = pitch.bin_statistic(x_coords, y_coords, statistic='count', bins=(6, 5))
        
        # Normalize the data for coloring dynamically based on actual data
        max_challenges = np.max(bin_statistic['statistic'])
        norm = Normalize(vmin=0, vmax=max_challenges)
        cmap = plt.cm.Reds
        
        # Plot the colored squares
        pc = pitch.heatmap(bin_statistic, ax=ax, cmap=cmap, edgecolors='black', alpha=0.7, vmin=0, vmax=max_challenges)
        
        # Add text annotations for each bin
        for i in range(bin_statistic['statistic'].shape[0]):
            for j in range(bin_statistic['statistic'].shape[1]):
                bin_count = bin_statistic['statistic'][i, j]
                if bin_count > 0:  # Only annotate non-zero bins
                    bin_center = bin_statistic['cx'][i, j], bin_statistic['cy'][i, j]
                    ax.text(bin_center[0], bin_center[1], str(int(bin_count)),
                            ha='center', va='center', fontsize=12, color='black')
        
        # Add a color scale using matplotlib directly
        sm = ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax)
        cbar.set_label(f'Number of aerial challenges lost', fontsize=12)
    
    # Display the total number of aerial challenges lost in the tournament and by the team
    ax.text(0.5, 1.05, f"Total aerial challenges lost in matches played by {team_name}: {total_aerial_challenges_lost_in_matches}", ha='center', va='center', transform=ax.transAxes, fontsize=12, color='black')
    ax.text(0.5, 1.10, f"Total aerial challenges lost by {team_name}: {total_team_aerial_challenges_lost}", ha='center', va='center', transform=ax.transAxes, fontsize=12, color='black')
    
    # Set title
    #ax.set_title(f"{team_name} Aerial Challenges Lost Map in Tournament", fontsize=15)
    
    plt.tight_layout()
    plt.show()

# Parameters
teams = ["Sweden Women's"]
competition_id = 72  # competition ID
season_id = 30  # season ID

# Plot aerial challenges lost for the teams in the tournament
for team in teams:
    plot_aerial_challenges_lost_for_team_in_tournament(team, competition_id, season_id)
