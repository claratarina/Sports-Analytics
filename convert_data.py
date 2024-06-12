import pandas as pd

# Define the data for each team in each tournament
data = {
    'tournament': ['World Cup 2023', 'World Cup 2023', 'World Cup 2023', 'Euros 2022', 'Euros 2022', 'Euros 2022', 'World Cup 2019', 'World Cup 2019', 'World Cup 2019'],
    'competition_id': [72, 72, 72, 53, 53, 53, 72, 72, 72],
    'season_id': [107, 107, 107, 106, 106, 106, 30, 30, 30],
    'team': ['Spain', 'England', 'Sweden', 'England', 'Germany', 'Sweden', 'USA', 'Netherlands', 'Sweden'],
    'successful_passes_pct': [81.5, 82.6, 75.2, 80.8, 75.0, 74.4, 77.0, 76.9, 75.3],
    'avg_goals_per_match': [2.42, 1.857, 2, 3.5, 2.33, 1.6, 3.57, 1.57, 1.7],
    'total_goals': [17, 13, 14, 21, 14, 8, 25, 11, 12],
    'total_shots': [158, 94, 85, 108, 107, 88, 130, 86, 105],
    'xG for total shots': [17.8, 9.6, 11.78, 15.8, 11.66, 10.87, 16.5, 9.92, 10.46],
    'total_touches_final_third': [5659, 4045, 3573, 2930, 3051, 2567, 3797, 3600, 3439],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
csv_file = 'WC23.csv'
df.to_csv(csv_file, index=False)
print(f'Data saved to {csv_file}')


