import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Radar

# Data WC 23
'''data = {
    'team': ['Sweden', 'England', 'Spain'],
    'total_goals': [14, 13, 17],
    'average_goals_per_match': [2, 1.85, 2.42],
    'total_shots': [11.82, 13, 21.6],
    'shots_on_target': [4.25, 5.57, 6.85],
    'ball_possession': [51.11, 59.02, 65.72],
    'total_passes': [468.6, 584.28, 702.57],
    'total_successful_passes': [353.1, 483.71, 574.53],
    'shots_from_corner': [2.5, 3.39, 5.25],
    'shots_from_free_kick': [2.53, 1.17, 2],
    'shots_from_penalty': [0.42, 0.14, 0.39],
    'xG_for_total_shots': [1.66, 1.34, 2.44],
    'Ball_recovery': [31.07, 29.07, 44.78]
}'''

#data WC19
'''data = {
    'team': ['Sweden', 'Netherlands', 'USA'],
    'total_goals': [12, 11, 26],
    'average_goals_per_match': [1.7, 1.57, 3.71],
    'total_shots': [14.6, 11.71, 18.57],
    'shots_on_target': [5.2, 3.75, 7.71],
    'ball_possession': [50.17, 56.53, 60.33],
    'total_passes': [431.6, 535.64, 502.42],
    'total_successful_passes': [326.4, 413.25, 387.14],
    'shots_from_corner': [2.46, 1.46, 4.42],
    'shots_from_free_kick': [1.9, 2.32, 2.42],
    'shots_from_penalty': [0.14, 0.14, 0.57],
    'xG_for_total_shots': [1.466, 1.37, 2.35],
    'Ball_recovery': [28.57, 27.35, 35.85]
}'''



#data Euro22
data = {
    'team': ['Sweden', 'England', 'Germany'],
    'total_goals': [9, 22, 14],
    'average_goals_per_match': [1.8, 3.66, 2.33],
    'total_shots': [17.6, 17.04, 17.2],
    'shots_on_target': [5.8, 6.58, 4.875],
    'ball_possession': [56.59, 61.35, 52.50],
    'total_passes': [449.4, 513.54, 478.66],
    'total_successful_passes': [334.2, 417.45, 360.375],
    'shots_from_corner': [4.4, 3.04, 3.58],
    'shots_from_free_kick': [2.2, 1.75, 2.5],
    'shots_from_penalty': [0.2, 0.16, 0.0],
    'xG_for_total_shots': [2.174, 2.518, 1.87],
    'Ball_recovery': [38.6, 25.41, 37.87]
}



# Create a DataFrame
df = pd.DataFrame(data)

def plot_radar_chart(df, teams):
    data = df[df['team'].isin(teams)]
    
    if data.empty:
        print("No data available for the specified teams.")
        return

    params = [
        'Total Goals', 'Avg Goals', ' Avg Total Shots', ' Avg Shots on Target',
        'Ball Possession (%)', 'Avg Total Passes', 'Avg Total Successful Passes',
        'Avg Shots from Corner', 'Avg Shots from Free Kick', 'Avg Shots from Penalty', 'Sum of xG for Total Shots','Recovery/interception oponents half'
    ]
    
    min_values = [0, 0, 10, 2, 40, 400, 300, 1, 1, 0, 1, 0]
    max_values = [20, 3, 25, 10, 70, 800, 600, 6, 4, 1, 3, 100]
    
    radar = Radar(params, min_values, max_values, lower_is_better=[], num_rings=10, ring_width=1, center_circle_radius=2)
    
    fig, (ax_radar, ax_table) = plt.subplots(nrows=1, ncols=2, figsize=(14, 6), gridspec_kw={'width_ratios': [2, 1]})
    
    radar._setup_axis(ax=ax_radar, facecolor='#ffffff')  
    radar.draw_circles(ax=ax_radar, facecolor='#D3D3D3', edgecolor='#D3D3D3')
    radar.draw_range_labels(ax=ax_radar, fontsize=8)
    radar.draw_param_labels(ax=ax_radar, fontsize=8)
    
    if len(teams) == 1:
        team = teams[0]
        team_data = data[data['team'] == team]
        
        if team_data.empty:
            print(f"No data available for team {team}.")
            return
        
        team_data = team_data.iloc[0]
        
        values = [
            team_data['total_goals'], 
            team_data['average_goals_per_match'], 
            team_data['total_shots'], 
            team_data['shots_on_target'], 
            team_data['ball_possession'], 
            team_data['total_passes'], 
            team_data['total_successful_passes'],
            team_data['shots_from_corner'], 
            team_data['shots_from_free_kick'], 
            team_data['shots_from_penalty'], 
            team_data['xG_for_total_shots'],
            team_data['Ball_recovery']
        ]
        
        radar_output = radar.draw_radar(values, ax=ax_radar, kwargs_radar={'facecolor': '#00f2c1', 'alpha': 0.6})
        radar_poly, vertices = radar_output
        
       
        ax_radar.legend([radar_poly], [team], loc='upper right', fontsize=15)
        
        
        table_data = [[team, value] for param, value in zip(params, values)]
        table = ax_table.table(cellText=table_data, colLabels=['Metric', 'Value'], loc='center', colWidths=[0.4, 0.3])
        table.scale(1, 1.5)
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        ax_table.axis('off')
        
    elif len(teams) == 2:
        
        team1, team2 = teams
        
        team1_data = data[data['team'] == team1]
        team2_data = data[data['team'] == team2]
        
        if team1_data.empty or team2_data.empty:
            if team1_data.empty:
                print(f"No data available for team {team1}.")
            if team2_data.empty:
                print(f"No data available for team {team2}.")
            return
        
        team1_data = team1_data.iloc[0]
        team2_data = team2_data.iloc[0]
        
        values1 = [
            team1_data['total_goals'], 
            team1_data['average_goals_per_match'], 
            team1_data['total_shots'], 
            team1_data['shots_on_target'], 
            team1_data['ball_possession'], 
            team1_data['total_passes'], 
            team1_data['total_successful_passes'],
            team1_data['shots_from_corner'], 
            team1_data['shots_from_free_kick'], 
            team1_data['shots_from_penalty'], 
            team1_data['xG_for_total_shots'],
            team1_data['Ball_recovery']
        ]
        
        values2 = [
            team2_data['total_goals'], 
            team2_data['average_goals_per_match'], 
            team2_data['total_shots'], 
            team2_data['shots_on_target'], 
            team2_data['ball_possession'], 
            team2_data['total_passes'], 
            team2_data['total_successful_passes'],
            team2_data['shots_from_corner'], 
            team2_data['shots_from_free_kick'], 
            team2_data['shots_from_penalty'], 
            team2_data['xG_for_total_shots'],
            team2_data['Ball_recovery']
        ]
        
        radar_output = radar.draw_radar_compare(values1, values2, ax=ax_radar,
                                                kwargs_radar={'facecolor': '#00f2c1', 'alpha': 0.6},
                                                kwargs_compare={'facecolor': '#d80499', 'alpha': 0.6})
        radar_poly, radar_poly2, vertices1, vertices2 = radar_output
        
        
        ax_radar.legend([radar_poly, radar_poly2], [team1, team2], loc='lower left', fontsize=8)
        
        table_data = [[param, value1, value2] for param, value1, value2 in zip(params, values1, values2)]
        table = ax_table.table(cellText=table_data, colLabels=['Metric', f'{team1}', f'{team2}'], loc='center', colWidths=[0.8, 0.3, 0.3])
        table.scale(1, 1.5)
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        ax_table.axis('off')
        
    else:
        print("Please provide one or two teams for comparison.")
        return
    
    
    plt.title(f'Euros 2022', fontsize=20, fontweight='bold')
    
    plt.show()


plot_radar_chart(df, ['Germany', 'Sweden'])
