import requests

def fetch_matches(competition_id, season_id):
    matches_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/{competition_id}/{season_id}.json'
    response = requests.get(matches_url)
    return response.json()

def fetch_match_events(match_id):
    events_url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json'
    response = requests.get(events_url)
    return response.json()

def count_passes_and_successful_passes(team_name, competition_id, season_id):
    matches_data = fetch_matches(competition_id, season_id)
    match_passes = []

    for match in matches_data:
        if team_name in [match['home_team']['home_team_name'], match['away_team']['away_team_name']]:
            match_id = match['match_id']
            opponent_team = match['away_team']['away_team_name'] if team_name == match['home_team']['home_team_name'] else match['home_team']['home_team_name']
            match_events = fetch_match_events(match_id)
            
            total_passes = 0
            successful_passes = 0

            for event in match_events:
                if 'possession_team' in event and event['possession_team']['name'] == team_name and event['type']['name'] == 'Pass':
                    total_passes += 1
                    if 'pass' in event and ('outcome' not in event['pass'] or event['pass']['outcome'] is None):
                        successful_passes += 1

            match_passes.append({
                "match_id": match_id,
                "opponent_team": opponent_team,
                "total_passes": total_passes,
                "successful_passes": successful_passes
            })

    return match_passes

# Example usage:
team_name = "Germany Women's"
competition_id = 53  # Example competition ID
season_id = 106  # Example season ID

passes_data = count_passes_and_successful_passes(team_name, competition_id, season_id)

for match in passes_data:
    print(f"Match ID {match['match_id']}: Opponent = {match['opponent_team']}, Total Passes = {match['total_passes']}, Successful Passes = {match['successful_passes']}")
