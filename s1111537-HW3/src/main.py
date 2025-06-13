import constant, dataloader, dataprocessor, visualizer

PLAYER_FILE_PATH = constant.filePath.PLAYER_CSV.value
TEAM_FILE_PATH = constant.filePath.TEAM_CSV.value

if __name__ == '__main__':
    player_df = dataloader.load_data(PLAYER_FILE_PATH)
    team_df = dataloader.load_data(TEAM_FILE_PATH)

    dataprocessor.mapping_abbr(player_df) # Because Team in player dataframe is abbreviation, we need to map it to its full name
    team_by_year = dataprocessor.find_top_bottom_teams_by_year(team_df)# The team which has the highest or the lowest winrate in each year
    pitcher_era = dataprocessor.get_era_by_team(player_df, team_by_year)
    visualizer.plot_era_histogram(pitcher_era[0])
    visualizer.plot_era_histogram(pitcher_era[1])
