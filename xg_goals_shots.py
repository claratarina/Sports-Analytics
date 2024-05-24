import requests
import matplotlib.pyplot as plt
from mplsoccer import Pitch

def plot_goal_shot_locations(match_events, match_id):
    # Filter shot events made by Sweden in periods 1 to 4
    sweeden_events = [event for event in match_events if event['team']['name'] == "Spain Women's" and event['period'] in range(1, 5)]

    # Filter shot events
    shot_events = [event for event in sweeden_events if 'shot' in event]

    # Plot location of all shots
    fig, ax = plt.figure(figsize=(10, 7)), plt.gca()
    pitch = Pitch(pitch_type='statsbomb')
    pitch.draw(ax=ax)
    
    goal_players = []
    total_goals = 0
    total_xG = 0.0
    home_team_name = match_events[0]['team']['name']
    away_team_name = match_events[1]['team']['name']
    
    for event in shot_events:
        xG = event['shot'].get('statsbomb_xg', 0)  # Get xG value, default to 0 if not available
        total_xG += xG
        shot_type_name = event['shot']['type']['name'] if 'type' in event['shot'] else 'Unknown'
        if 'outcome' in event['shot'] and event['shot']['outcome']['name'] == 'Goal':
            total_goals += 1
            player_name = event['player']['name']
            goal_players.append((player_name, xG, shot_type_name))
            # Plot shots that resulted in goals in red and annotate with xG and shot type
            ax.plot(event['location'][0], event['location'][1], 'ro', markersize=10)
            ax.annotate(f"{xG:.2f}, {shot_type_name}", (event['location'][0], event['location'][1]), 
                        textcoords="offset points", xytext=(0,10), ha='center', color='black', fontsize=7, fontweight='regular')
        else:
            # Plot shots that did not result in goals in blue and annotate with xG
            ax.plot(event['location'][0], event['location'][1], 'bo', markersize=5)
            ax.annotate(f"{xG:.2f}", (event['location'][0], event['location'][1]), 
                        textcoords="offset points", xytext=(0,5), ha='center', color='grey', fontsize=7, fontweight='regular')
    
    # Constructing the player name, xG, and shot type string for goals
    player_info_str = '\n'.join([f"{name}: xG {xG:.2f}, Shot type: {shot_type}" for name, xG, shot_type in goal_players])
    # Display player names, xG values, and shot types outside the field
    ax.text(0.5, -0.15, f"Goals with xG and shot type:\n{player_info_str}", 
            horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=10)
    
    # Add match information and goal/xG summary to the title
    match_info_str = f"Match ID: {match_id}, Home Team: {home_team_name}, Away Team: {away_team_name}"
    summary_str = f"Total Goals: {total_goals}, ∑(xG for total shots): {total_xG:.2f}"
    ax.set_title(f"{match_info_str}\n{summary_str}", fontsize=12)

# List of example match IDs
match_ids = [3906390, 3904628, 3893806, 3893822, 3902240, 3901733, 3893791]  # Example match IDs
# Fetch events data for each match and plot the shot locations
for match_id in match_ids:
    # Fetch events data for the match
    events_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json'
    response = requests.get(events_url)
    match_events = response.json()
    
    # Plot all shot locations with shots resulting in goals annotated
    plot_goal_shot_locations(match_events, match_id)

plt.show()
