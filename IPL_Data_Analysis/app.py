import pandas as pd
import streamlit as st
import data_preprocessor, helper
from helper import season_wise_analysis, fetch_final_scores, plot_ipl_champions, plot_venues_per_season, plot_team_win_percentages, plot_top_run_scorers, plot_top_bowlers_by_overs, plot_top_boundaries
import matplotlib.pyplot as plt
import seaborn as sns

matches, deliveries = data_preprocessor.data_preprocess()

st.sidebar.image("IPL_Logo.png", use_container_width=True) 
st.sidebar.markdown(
    "<h2 style='font-weight: bold; color: navy;'>IPL Match Analysis (2008-2024)</h12",
    unsafe_allow_html=True
)

user_menu = st.sidebar.radio('Select an Option', ('Overall Analysis', 'Season-Wise Analysis', 'Team-Wise Analysis', 'Player-Wise Analysis'))

if user_menu == 'Overall Analysis':
    st.title("Analysis of All Seasons")
    teams_df = matches['fielding'].unique().tolist()

    teams_df = pd.DataFrame({'Team Name': teams_df})
    teams_df.index = teams_df.index + 1
    teams_df.index.name = 'S.No.'
    st.subheader("Team List")
    st.dataframe(teams_df, use_container_width=True, height=300)

    st.subheader("Number of Winning Matches of All Seasons by Every Team")
    winning_matches = matches.groupby(['season', 'winner']).size().reset_index(name='winning_count')
    winning_matches = winning_matches.pivot(index='season', columns='winner', values='winning_count').fillna(0).astype(int)
    winning_matches = winning_matches.reindex(sorted(winning_matches.columns), axis=1)
    winning_matches['Total Winning Matches'] = winning_matches.sum(axis=1)
    st.dataframe(winning_matches, use_container_width=True, height=300)

if user_menu == 'Season-Wise Analysis':
    st.title("Season Wise Analysis of IPL")
    season_wise_analysis(matches)

    st.subheader("Final Match Scores")
    final_scores = helper.fetch_final_scores(matches, deliveries)
    st.dataframe(final_scores, use_container_width=True, height=300)

    # Call the visualization function
    helper.plot_final_scores(final_scores)
    
    # Match Played
    helper.match_played(matches)
    
    # Champions
    helper.plot_ipl_champions(matches)
    
    # Venues Per Match
    helper.plot_venues_per_season(matches)
    
# Team-Wise Analysis    
if user_menu == 'Team-Wise Analysis':
    helper.plot_team_win_percentages(matches)
    
    # Top Players
    helper.teamwise_top_players(deliveries)
    
# Player Wise Analysis    
if user_menu == 'Player-Wise Analysis':
    # Top Batsman
    helper.plot_top_run_scorers(deliveries) 
    
    # Top Bowlers
    helper.plot_top_bowlers_by_overs(deliveries) 
    
    # Top 6's and 4's Hit
    helper.plot_top_boundaries(deliveries) 
    
    # Best Strike Rates
    helper.plot_best_strike_rates(deliveries)

    # Most Wickets
    helper.plot_most_wickets(deliveries)

    # Most Dismissals
    helper.plot_fielding_dismissals(deliveries)
    