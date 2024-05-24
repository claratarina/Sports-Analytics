import matplotlib.pyplot as plt
from soccerplots.radar_chart import Radar

# parameter names
params = ['xAssists', 'Key Passes', 'Crosses Into Box', 'Cross Competion', 'Deep Completions',
          'Progressive Passes', 'Prog. Passes Accuracy%', 'Dribbles', 'Progressive Runs',
          'PADJ Interceptions', 'Succ. Def Actions', 'Def Duel Win%']

# range values
ranges = [(0.0, 0.15), (0.0, 0.67), (0.06, 0.63), (19.51, 50.0), (0.35, 1.61), (6.45, 11.94), (62.94, 79.46), (0.43, 4.08), (0.6, 2.33), (5.01, 7.2), (9.02, 12.48),
          (52.44, 66.67)]

# parameter values for each team
values = [
    # Team 1 (e.g., AFC Ajax)
    [0.11, 0.53, 0.70, 27.66, 1.05, 6.84, 84.62, 4.56,
        2.22, 5.93, 8.88, 64.29],

    # Team 2 (e.g., Barcelona)
    [0.07, 0.36, 0.16, 32.14, 1.04, 7.37, 74.46, 3.68,
        2.40, 6.87, 8.97, 61.14]
]

# Title and subtitle for each team
title = dict(
    title_name='AFC Ajax',
    title_color='#B6282F',
    subtitle_name='Team 1 Subtitle',
    subtitle_color='#B6282F',
    title_name_2='Barcelona',
    title_color_2='#344D94',
    subtitle_name_2='Team 2 Subtitle',
    subtitle_color_2='#344D94',
    title_fontsize=18,
    subtitle_fontsize=15,
)

# instantiate object
radar = Radar()

# plot radar for two teams
fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values,
                           radar_color=['#B6282F', '#344D94'],
                           alphas=[0.8, 0.6], title=title,
                           compare=True)
plt.show()

