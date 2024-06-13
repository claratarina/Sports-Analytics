import requests
import matplotlib.pyplot as plt
from mplsoccer import Pitch

def plot_events(ax, events, team_name, color, marker):
    pass_locations = []
    assist_location = None
    for event in events:
        if event['type']['name'] == 'Pass':
            pass_location = event['location']
            player_name = event['player']['name']
            pass_locations.append(pass_location)
            ax.plot(pass_location[0], pass_location[1], color, marker=marker, markersize=7)
            ax.text(pass_location[0], pass_location[1], player_name, color='black', fontsize=7, ha='center', va='center')
            assist_location = pass_location
        elif event['type']['name'] == 'Corner':
            corner_location = event['location']
            player_name = event['player']['name']
            ax.plot(corner_location[0], corner_location[1], 'green', marker='o', markersize=7)
            ax.text(corner_location[0], corner_location[1], player_name, color='black', fontsize=7, ha='center', va='center')
            assist_location = corner_location
    return assist_location, pass_locations

def plot_goals(match_events, match_id, num_cols, num_rows):
    sweden_goal_events = [event for event in match_events if event['team']['name'] == "Sweden Women's" and event['type']['name'] == 'Shot' and 'outcome' in event['shot'] and event['shot']['outcome']['name'] == 'Goal']
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(16, 8))
    axs = axs.flatten()
    for i, goal_event in enumerate(sweden_goal_events):
        goal_location = goal_event['location']
        assist_location = None
        assist_player = None
        pass_locations = []
        goal_possession_id = goal_event['possession']
        preceding_events = [event for event in match_events if event['possession'] == goal_possession_id]
        pitch = Pitch(pitch_type='statsbomb')
        pitch.draw(ax=axs[i])
        assist_location, pass_locations = plot_events(axs[i], preceding_events, "Sweden Women's", 'blue', 'o')
        if pass_locations:
            pass_xs, pass_ys = zip(*pass_locations)
            axs[i].plot(pass_xs, pass_ys, 'blue')
        if assist_location and assist_location != goal_location:
            axs[i].plot([assist_location[0], goal_location[0]], [assist_location[1], goal_location[1]], 'pink')
        goal_player = goal_event['player']['name']
        xG = goal_event['shot']['statsbomb_xg']
        axs[i].plot(goal_location[0], goal_location[1], 'ro', markersize=10)
        axs[i].text(goal_location[0], goal_location[1], f"{goal_player} (xG: {xG:.2f})", color='black', fontsize=7, ha='center', va='center')
        axs[i].text(goal_location[0], goal_location[1] - 1, "Goal", color='black', fontsize=7, ha='center', va='center')
        home_team_name = match_events[0]['team']['name']
        away_team_name = match_events[1]['team']['name']
        match_info_str = f"Match ID: {match_id}, Home Team: {home_team_name}, Away Team: {away_team_name}"
        axs[i].set_title(match_info_str, fontsize=10, pad=15)
    for j in range(len(sweden_goal_events), num_cols * num_rows):
        axs[j].axis('off')
    plt.tight_layout()
    plt.show()

match_ids = [3893796, 3893814, 3893830, 3901797, 3902239, 3904628, 3906389
]

for match_id in match_ids:
    events_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json'
    response = requests.get(events_url)
    match_events = response.json()
    sweden_goal_events = [event for event in match_events if event['team']['name'] == "Sweden Women's" and event['type']['name'] == 'Shot' and 'outcome' in event['shot'] and event['shot']['outcome']['name'] == 'Goal']
    num_goals = len(sweden_goal_events)
    num_cols = 2
    num_rows = (num_goals + 1) // num_cols + ((num_goals + 1) % num_cols != 0)
    plot_goals(match_events, match_id, num_cols, num_rows)
