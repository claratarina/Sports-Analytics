import requests

def calculate_possession(match_events, team_name):
    possession_time = 0
    possession_start_time = None
    last_possession_team = None

    for event in match_events:
        if 'possession_team' in event:
            possession_team = event['possession_team']['name']
            minute = event['minute']
            second = event['second']

            if possession_team == last_possession_team:
                continue

            if possession_team == team_name:
                possession_start_time = minute * 60 + second
            else:
                if last_possession_team == team_name and possession_start_time is not None:
                    possession_time += (minute * 60 + second) - possession_start_time

            last_possession_team = possession_team

    # If the match ended while the specified team had possession
    if last_possession_team == team_name and possession_start_time is not None:
        possession_time += (match_events[-1]['minute'] * 60 + match_events[-1]['second']) - possession_start_time

    return possession_time

def get_match_events(match_id):
    # Fetch events data for the given match ID
    events_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json'
    response = requests.get(events_url)
    match_events = response.json()
    return match_events

def get_matches(competition_id, season_id):
    # Fetch matches data for the given competition and season ID
    matches_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/{competition_id}/{season_id}.json'
    response = requests.get(matches_url)
    matches_data = response.json()
    return matches_data

# Example usage:
team_name = "Spain Women's"
competition_id = 72
season_id = 107

# Get matches for the competition and season
matches = get_matches(competition_id, season_id)

# Filter matches to include only those where the Women's team is playing
team_matches = [match for match in matches if match['home_team']['home_team_name'] == team_name or match['away_team']['away_team_name'] == team_name]

# Initialize list for possession percentages
possession_percentages = []

# Process each match where the team is playing
for match in team_matches:
    match_id = match['match_id']
    home_team = match['home_team']['home_team_name']
    away_team = match['away_team']['away_team_name']
    opponent_team = away_team if home_team == team_name else home_team
    
    match_events = get_match_events(match_id)

    # Calculate total match duration
    match_duration = (match_events[-1]['minute'] * 60 + match_events[-1]['second']) - (match_events[0]['minute'] * 60 + match_events[0]['second'])
    print(f"Match ID: {match_id}, Match Duration: {match_duration} seconds, Opponent: {opponent_team}")

    # Calculate possession time for the specified team
    possession_time = calculate_possession(match_events, team_name)
    print(f"Match ID: {match_id}, Possession Time for {team_name}: {possession_time} seconds, Opponent: {opponent_team}")

    # Calculate possession percentage for the match
    possession_percentage = (possession_time / match_duration) * 100
    possession_percentages.append(possession_percentage)
    print(f"Match ID: {match_id}, Possession Percentage for {team_name}: {possession_percentage:.2f}%, Opponent: {opponent_team}")

# Calculate mean possession percentage
mean_possession_percentage = sum(possession_percentages) / len(possession_percentages)

print(f"{team_name} mean possession percentage in competition ID {competition_id}, season ID {season_id}: {mean_possession_percentage:.2f}%")
