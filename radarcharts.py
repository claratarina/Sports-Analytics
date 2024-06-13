import pandas as pd
from mplsoccer import Radar
import matplotlib.pyplot as plt
import os

def clear_terminal():
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

# Clear the terminal before starting
clear_terminal()

# Read the data from CSV
df = pd.read_csv('team_performance_data.csv')

# Function to plot radar chart for one or two teams
def plot_radar_chart(df, teams, competition_id, season_id):
    # Filter the data for the specified competition_id and season_id
    data = df[(df['competition_id'] == competition_id) & (df['season_id'] == season_id)]
    
    if data.empty:
        print("No data available for the specified competition_id and season_id.")
        return

    # Parameters for the radar chart
    params = ['Successful Passes (%)', 'Avg Goals Per Match', 'Total Goals', 'Total Shots', 'xG for total shots', 'Total Touches in Final Third']
    
    # Min and Max values for normalization
    min_values = [70, 1, 5, 50, 5, 2000]
    max_values = [100, 4, 30, 200, 20, 6000]
    
    # Instantiate the Radar class
    radar = Radar(params, min_values, max_values, lower_is_better=[], num_rings=10, ring_width=1, center_circle_radius=1)
    
    # Setup the plot
    fig, ax = radar.setup_axis()
    rings_inner = radar.draw_circles(ax=ax, facecolor='#D3D3D3', edgecolor='#D3D3D3')
    range_labels = radar.draw_range_labels(ax=ax, fontsize=10)
    param_labels = radar.draw_param_labels(ax=ax, fontsize=10)

    if len(teams) == 1:
        # Plot data for the single team
        team = teams[0]
        team_data = data[data['team'] == team]
        
        if team_data.empty:
            print(f"No data available for team {team} in the specified competition_id and season_id.")
            return
        
        team_data = team_data.iloc[0]
        
        values = [
            team_data['successful_passes_pct'], 
            team_data['avg_goals_per_match'] if pd.notnull(team_data['avg_goals_per_match']) else 0, 
            team_data['total_goals'], 
            team_data['total_shots'], 
            team_data['xG for total shots'], 
            team_data['total_touches_final_third']
        ]
        
        radar_output = radar.draw_radar(values, ax=ax, kwargs_radar={'facecolor': '#00f2c1', 'alpha': 0.6})
        
        radar_poly, vertices = radar_output
        
        # Add legend
        ax.legend([radar_poly], [team], loc='upper right', fontsize=15)
        
    elif len(teams) == 2:
        # Plot data for the two teams for comparison
        team1, team2 = teams
        
        team1_data = data[data['team'] == team1]
        team2_data = data[data['team'] == team2]
        
        if team1_data.empty or team2_data.empty:
            if team1_data.empty:
                print(f"No data available for team {team1} in the specified competition_id and season_id.")
            if team2_data.empty:
                print(f"No data available for team {team2} in the specified competition_id and season_id.")
            return
        
        team1_data = team1_data.iloc[0]
        team2_data = team2_data.iloc[0]
        
        values1 = [
            team1_data['successful_passes_pct'], 
            team1_data['avg_goals_per_match'] if pd.notnull(team1_data['avg_goals_per_match']) else 0, 
            team1_data['total_goals'], 
            team1_data['total_shots'], 
            team1_data['xG for total shots'], 
            team1_data['total_touches_final_third']
        ]
        
        values2 = [
            team2_data['successful_passes_pct'], 
            team2_data['avg_goals_per_match'] if pd.notnull(team2_data['avg_goals_per_match']) else 0, 
            team2_data['total_goals'], 
            team2_data['total_shots'], 
            team2_data['xG for total shots'], 
            team2_data['total_touches_final_third']
        ]
        
        radar_output = radar.draw_radar_compare(values1, values2, ax=ax,
                                                kwargs_radar={'facecolor': '#00f2c1', 'alpha': 0.6},
                                                kwargs_compare={'facecolor': '#d80499', 'alpha': 0.6})
        
        radar_poly, radar_poly2, vertices1, vertices2 = radar_output
        
        # Add legend
        ax.legend([radar_poly, radar_poly2], [team1, team2], loc='lower left', fontsize=10)
        
    else:
        print("Please provide one or two teams for comparison.")
        return
    
    # Add title with competition and year
    if competition_id == 72:  # World Cup
        year = 2023 if season_id == 107 else 2019
        competition_name = 'World Cup'
    else:  # Euros
        year = 2022 if season_id == 106 else 2017
        competition_name = 'Euros'
    
    plt.title(f'{competition_name} {year}', fontsize=20, fontweight='bold')
    
    plt.show()

# Example usage
plot_radar_chart(df, ['England', 'Sweden'], 72, 107)
#plot_radar_chart(df, ['Spain'], 72, 107)
