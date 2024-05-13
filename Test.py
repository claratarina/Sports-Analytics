import json
from statsbombpy import sb

# Read JSON data from file with error handling
with open('107.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    # Read JSON data from file with error handling
with open('3901797.json', 'r', encoding='utf-8') as file:
    event = json.load(file)


# Specify the country/team you want to filter for
desired_country = "Sweden"

# Collect matches involving the specified country/team
matches = []
for match in data:
    home_team = match['home_team']['country']['name']
    away_team = match['away_team']['country']['name']
    if home_team == desired_country or away_team == desired_country:
        matches.append(match)

# Now 'matches' contains all the data for matches involving the specified country/team
# You can further process or print the data as per your requirements
for match in matches:
    print("Match ID:", match['match_id'])
    print("Match Date:", match['match_date'])
    print("Kick Off:", match['kick_off'])
    print("Home Team:", match['home_team']['home_team_name'])
    print("Away Team:", match['away_team']['away_team_name'])
    print("Home Score:", match['home_score'])
    print("Away Score:", match['away_score'])
    print()  # Just for spacing between matches

