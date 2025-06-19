import pandas as pd 
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# Season Wise Analysis
def season_wise_analysis(ipl_match_df):
    seasons = ipl_match_df[ipl_match_df['match_type'] == 'Final']
    season_data = seasons[['season','winner','venue','toss_winner','toss_decision']].reset_index(drop=True)
    season_data.index = season_data.index + 1
    season_data.index.name = 'S.No.'
    season_data.columns = ['Season', 'Winner', 'Venue', 'Toss Winner', 'Toss Decision']

    # Display full table first (existing behavior)
    st.subheader("Complete Season Summary")
    st.dataframe(season_data, use_container_width=True, height=300)

    # Enhancement: Dropdown to select season
    st.sidebar.subheader("Season-wise Details")
    available_seasons = season_data['Season'].unique().tolist()
    selected_season = st.sidebar.selectbox("Select a Season", sorted(available_seasons))

    # Filter data for selected season
    selected_data = season_data[season_data['Season'] == selected_season]

    # Display selected season's information
    st.subheader(f"**Details for Season {selected_season}:**")
    st.dataframe(selected_data, use_container_width=True, height=50)

    winner = selected_data.iloc[0]['Winner']
    st.success(f" Winner: {winner}")
    
# Final Score Table Data
def fetch_final_scores(matches, deliveries):
    # Filter only finals
    finals = matches[matches['match_type'] == 'Final']
    
    final_scores = []

    for _, row in finals.iterrows():
        match_id = row['match_id']
        season = row['season']
        
        # Get deliveries for that final match
        match_deliveries = deliveries[deliveries['match_id'] == match_id]
        
        # Calculate total runs for each team in that final
        team_scores = match_deliveries.groupby('batting_team')['total_runs'].sum().reset_index()
        team_scores.columns = ['Team', 'Score']
        team_scores['Season'] = season
        
        final_scores.append(team_scores)

    # Convert list of dfs into a single dataframe
    final_scores_df = pd.concat(final_scores, ignore_index=True)
    
    return final_scores_df

# Final Score Plot
def plot_final_scores(final_scores_df):
    
    if final_scores_df.empty:
        st.warning("No data available to plot.")
        return

    # Sort seasons for better x-axis display
    final_scores_df = final_scores_df.sort_values(by='Season')

    # Plot
    fig = px.bar(
        final_scores_df,
        x='Season',
        y='Score',
        color='Team',
        barmode='group',
        text='Score',
        title="IPL Final Match Scores (Season-wise)",
        color_discrete_sequence=px.colors.qualitative.Set3,
        width=1100,   # wider chart
        height=650
    )

    # Professional Bar Width Control: reduce bargap for thicker bars
    fig.update_layout(
        bargap=0.01,   # THICKER bars => more professional look
        xaxis_title="Season",
        yaxis_title="Total Score",
        title_font_size=24,
        xaxis=dict(tickmode='linear', tickfont=dict(size=14)),
        yaxis=dict(tickfont=dict(size=14)),
        legend=dict(font=dict(size=14)),
        margin=dict(l=40, r=40, t=80, b=80)
    )

    # Data labels outside bars with clear font size
    fig.update_traces(
        textposition='outside',
        textfont_size=12
    )

    # Give some headroom above bars for text
    fig.update_yaxes(range=[0, final_scores_df['Score'].max() + 50])

    st.plotly_chart(fig, use_container_width=True)

# Played Match
def match_played(ipl_match_df):
    st.subheader("Matches Played Per Season")

    # Count matches per season
    match_counts = ipl_match_df['season'].value_counts().sort_index().reset_index()
 
    # Rename properly
    match_counts.columns = ['Season', 'Number of Matches']

    # Ensure correct types
    match_counts['Season'] = match_counts['Season'].astype(int)
    match_counts = match_counts.sort_values(by='Season').reset_index(drop=True)

    # Show table
    st.dataframe(match_counts, use_container_width=True, height=300)

    # Plot
    fig = px.line(
        match_counts,
        x='Season',
        y='Number of Matches',
        markers=True,
        title="Total IPL Matches Played Per Season",
        labels={'Season': 'Season', 'Number of Matches': 'Match Count'},
        template="plotly_white"
    )

    fig.update_traces(
        line=dict(color='royalblue', width=3),
        marker=dict(size=8, color='crimson'),
        text=match_counts["Number of Matches"],
        textposition="top center"
    )

    fig.update_layout(
        title_font_size=22,
        xaxis=dict(tickmode='linear', tickfont=dict(size=14)),
        yaxis=dict(tickfont=dict(size=14)),
        hoverlabel=dict(bgcolor="white", font_size=14),
        margin=dict(l=40, r=40, t=80, b=60),
        height=550
    )

    st.plotly_chart(fig, use_container_width=True)

# Season Champions     
def plot_ipl_champions(matches_df):
    st.subheader("IPL Champions by Season")

    # Filter only FINAL matches
    final_matches = matches_df[matches_df['match_type'].str.lower() == 'final'].dropna(subset=['winner'])

    # Extract final winners per season
    season_winners = final_matches[['season', 'winner']].rename(columns={'season': 'Season', 'winner': 'Champion'})

    # Display season-wise champions table
    st.dataframe(season_winners.sort_values('Season'), use_container_width=True, height=300)

    # Count titles per team
    title_counts = season_winners['Champion'].value_counts().reset_index()
    title_counts.columns = ['Team', 'Titles Won']

    # Plot using Plotly Express
    fig = px.bar(
        title_counts,
        x='Titles Won',
        y='Team',
        orientation='h',
        text='Titles Won',
        color='Team',
        color_discrete_sequence=px.colors.qualitative.Safe,
        title=" Accurate IPL Titles Won by Each Team"
    )

    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Titles: %{x}",
        textposition='outside',
        marker=dict(line=dict(color="black", width=1.5))
    )

    fig.update_layout(
        xaxis=dict(title='Titles Won'),
        yaxis=dict(title='Team'),
        title=dict(x=0.5, font=dict(size=22)),
        hoverlabel=dict(bgcolor="white", font_size=14),
        margin=dict(l=40, r=40, t=80, b=60),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

# Venues    
def plot_venues_per_season(matches_df):
    st.subheader("Unique IPL Venues Used Per Season")

    # Group and rename columns
    venues_per_season = (
        matches_df.groupby('season')['venue']
        .nunique()
        .reset_index()
        .rename(columns={'season': 'Season', 'venue': 'Number of Venues'})
    )

    venues_per_season['Season'] = venues_per_season['Season'].astype(str)  # treat as category

    # Display table
    st.dataframe(venues_per_season, use_container_width=True, height=300)

    # Plot colorful bar chart using Season as color
    fig = px.bar(
        venues_per_season,
        x='Season',
        y='Number of Venues',
        text='Number of Venues',
        color='Season',  # categorical coloring
        color_discrete_sequence=px.colors.qualitative.Vivid,
        title=" Number of Unique IPL Venues Used Per Season",
        labels={'Number of Venues': 'Unique Venues'}
    )

    fig.update_traces(
        textposition='outside',
        hovertemplate="<b>Season %{x}</b><br>Venues: %{y}",
        marker_line=dict(color='black', width=1.2)
    )

    fig.update_layout(
        title_font_size=22,
        xaxis=dict(title='Season', tickmode='linear'),
        yaxis=dict(title='Unique Venue Count'),
        hoverlabel=dict(bgcolor="white", font_size=14),
        margin=dict(l=40, r=40, t=80, b=60),
        height=550,
        showlegend=False  # optional: hides redundant legend
    )

    st.plotly_chart(fig, use_container_width=True)
    
# Team Wise Analysis
def plot_team_win_percentages(matches_df):
    st.subheader("Team Win Performance Overview")

    # Count appearances
    batting = matches_df['batting'].value_counts()
    fielding = matches_df['fielding'].value_counts()
    total_matches = (batting + fielding).reset_index()
    total_matches.columns = ['Team', 'Total Matches']

    # Count wins
    wins = matches_df['winner'].value_counts().reset_index()
    wins.columns = ['Team', 'Wins']

    # Merge
    team_summary = pd.merge(total_matches, wins, on='Team', how='left')
    team_summary['Wins'] = team_summary['Wins'].fillna(0).astype(int)
    team_summary['Win %'] = (team_summary['Wins'] / team_summary['Total Matches']) * 100
    team_summary = team_summary.sort_values(by='Wins', ascending=False).reset_index(drop=True)

    # Display table
    st.dataframe(team_summary, use_container_width=True, height=350)

    # Pie Chart of Wins
    st.markdown("### Share of IPL Wins by Team")
    fig = px.pie(
        team_summary,
        names='Team',
        values='Wins',
        title='IPL Win Share by Team',
        color_discrete_sequence=px.colors.qualitative.Vivid,
        hole=0.3
    )

    fig.update_traces(
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Wins: %{value}<br>Share: %{percent}',
        pull=[0.05 if i == 0 else 0 for i in range(len(team_summary))]  # emphasize top team
    )

    fig.update_layout(
        height=600,
        margin=dict(t=80, b=60, l=30, r=30),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

# Top Players    
def teamwise_top_players(deliveries):
    st.subheader("Players in the Team")

    # Get unique teams
    teams = sorted(deliveries['batting_team'].unique())
    
    # Sidebar dropdown
    selected_team = st.sidebar.selectbox("Select a Team", teams)

    # Filter data for selected team
    team_data = deliveries[deliveries['batting_team'] == selected_team]

    # Group by batter and sum runs
    top_batters = team_data.groupby('batter')['batsman_runs'].sum().reset_index()
    top_batters = top_batters.sort_values(by='batsman_runs', ascending=False)
    top_batters.columns = ['Player', 'Total Runs']

    # Show table
    st.dataframe(top_batters, use_container_width=True, height=400)

    # Bar chart
    fig = px.bar(
        top_batters.head(10),
        x='Player',
        y='Total Runs',
        color='Total Runs',
        color_continuous_scale='Plasma',
        template='plotly_white',
        title=f"Top 10 Run Scorers for {selected_team}"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Player Wise Analysis
def plot_top_run_scorers(deliveries, top_n=10):
    st.subheader(f"Top Run Scorers in IPL")

    top_batsmen = (
        deliveries.groupby('batter')['batsman_runs']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={'batter': 'Player', 'batsman_runs': 'Runs'})
    )

    st.dataframe(top_batsmen, use_container_width=True, height=300)

    fig = px.bar(
        top_batsmen.head(10),
        x='Runs',
        y='Player',
        orientation='h',
        text='Runs',
        color='Player',
        color_discrete_sequence=px.colors.qualitative.Dark24,
        title=f"Top {top_n} IPL Run Scorers"
    )

    fig.update_traces(
        textposition='outside',
        hovertemplate="<b>%{y}</b><br>Runs: %{x}",
        marker_line=dict(color='black', width=1)
    )

    fig.update_layout(
        height=600,
        margin=dict(t=60, b=60),
        xaxis_title='Total Runs',
        yaxis_title='Player',
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
    
# Top Bowlers
def plot_top_bowlers_by_overs(deliveries):
    st.subheader("Top Bowlers by Total Overs Bowled")

    if 'bowler' not in deliveries.columns:
        st.error("Column 'bowler' not found in dataset")
        return

    # Count balls bowled by each bowler
    bowler_balls = deliveries.groupby('bowler').size().reset_index(name='Balls')

    # Convert balls to overs
    bowler_balls['Overs'] = (bowler_balls['Balls'] // 6) + (bowler_balls['Balls'] % 6) / 10

    # Sort top 10 bowlers
    top_bowlers = bowler_balls.sort_values(by='Balls', ascending=False)
    st.dataframe(top_bowlers, use_container_width=True, height=300)

    # Plot
    fig = px.bar(
        top_bowlers.head(10),
        x='bowler',
        y='Overs',
        color='Overs',
        color_continuous_scale='viridis',
        title='Top 10 Bowlers by Total Overs Bowled',
        hover_data={'Balls': True, 'Overs': ':.2f'}
    )
    fig.update_traces(hovertemplate="<b>%{x}</b><br>Overs: %{y:.2f}<br>Balls: %{customdata[0]}")
    fig.update_layout(xaxis_title="Bowler", yaxis_title="Overs", bargap=0.3)
    st.plotly_chart(fig, use_container_width=True)


# Top 6's and 4's Hit
def plot_top_boundaries(deliveries):
    st.subheader("Top Boundary Hitters (6s and 4s)")

    # Ensure required columns exist
    required_columns = ['batter', 'batsman_runs']
    for col in required_columns:
        if col not in deliveries.columns:
            st.error(f"Missing column: {col}")
            return

    # Count 6s and 4s
    sixes = deliveries[deliveries['batsman_runs'] == 6].groupby('batter').size().reset_index(name='6s')
    fours = deliveries[deliveries['batsman_runs'] == 4].groupby('batter').size().reset_index(name='4s')

    # Merge and compute total boundaries
    boundaries = pd.merge(sixes, fours, on='batter', how='outer').fillna(0)
    boundaries['6s'] = boundaries['6s'].astype(int)
    boundaries['4s'] = boundaries['4s'].astype(int)
    boundaries['Total Boundaries'] = boundaries['6s'] + boundaries['4s']
    
    # Top boundaries Hitter Table
    top_hitters_table = boundaries.sort_values(by='Total Boundaries', ascending=False)

    # Sort and get top 10
    top_hitters = boundaries.sort_values(by='Total Boundaries', ascending=False).head(10)

    # Display as table
    st.dataframe(top_hitters_table.rename(columns={
        'batsman': 'Player Name',
        '4s': 'Fours',
        '6s': 'Sixes'
    }).reset_index(drop=True), use_container_width=True)

    #Stacked bar chart
    melted = top_hitters.melt(id_vars='batter', value_vars=['4s', '6s'],
                              var_name='Boundary Type', value_name='Count')

    fig = px.bar(
        melted,
        x='batter',
        y='Count',
        color='Boundary Type',
        barmode='stack',
        title='Top 10 Players by Total 4s and 6s',
        color_discrete_map={'4s': 'orange', '6s': 'purple'}
    )
    fig.update_layout(xaxis_title="Player", yaxis_title="Count", bargap=0.3)
    fig.update_traces(hovertemplate="<b>%{x}</b><br>%{legendgroup}: %{y}")
    st.plotly_chart(fig, use_container_width=True)
    
# Best Strike Rates
def plot_best_strike_rates(deliveries):
    batsman_stats = deliveries.groupby('batter').agg({
        'batsman_runs': 'sum',
        'ball': 'count'
    }).rename(columns={'ball': 'Balls Faced'})
    batsman_stats['Strike Rate'] = (batsman_stats['batsman_runs'] / batsman_stats['Balls Faced']) * 100
    top_sr = batsman_stats.sort_values(by='Strike Rate', ascending=False).reset_index()

    st.subheader("Best Strike Rates")
    st.dataframe(top_sr.style.format({"Strike Rate": "{:.2f}"}))

    fig = px.bar(
        top_sr.head(10),
        x='batter',
        y='Strike Rate',
        color='Strike Rate',
        color_continuous_scale='Plasma',
        title="Top 10 Efficient Scorers ",
        template='simple_white'
        )

    fig.update_layout(
        xaxis_title="Batsman",
        yaxis_title="Strike Rate",
        title_font_size=20,
        title_x=0.5
        )

    st.plotly_chart(fig)


# Most Wickets
def plot_most_wickets(deliveries):
    wickets_df = deliveries[deliveries['player_dismissed'].notna()]
    top_wickets = wickets_df['bowler'].value_counts().reset_index()
    top_wickets.columns = ['Bowler', 'Wickets']

    st.subheader("Most Wickets")
    st.dataframe(top_wickets)

    fig = px.pie(top_wickets.head(10), values='Wickets', names='Bowler',
                 title='Top 10 Wicket Takers', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig)

# Most Dismissals
def plot_fielding_dismissals(deliveries):
    fielding_df = deliveries[deliveries['fielder'].notna()]
    dismissals = fielding_df['fielder'].value_counts().reset_index()
    dismissals.columns = ['Fielder', 'Dismissals']

    st.subheader("Most Fielding Dismissals")
    st.dataframe(dismissals)

    fig = px.bar_polar(dismissals.head(10), r='Dismissals', theta='Fielder',
                       color='Dismissals', title="Top Fielders by Dismissals",
                       color_continuous_scale=px.colors.sequential.Sunset)
    st.plotly_chart(fig)
