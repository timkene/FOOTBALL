import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# Initialize session state

def initialize_session_state():
    if 'teams' not in st.session_state:
        st.session_state.teams = {
            'Team A': ['Player A1', 'Player A2', 'Player A3', 'Player A4', 'Player A5'],
            'Team B': ['Player B1', 'Player B2', 'Player B3', 'Player B4', 'Player B5'],
            'Team C': ['Player C1', 'Player C2', 'Player C3', 'Player C4', 'Player C5'],
            'Team D': ['Player D1', 'Player D2', 'Player D3', 'Player D4', 'Player D5']
        }

    if 'matches' not in st.session_state:
        st.session_state.matches = []

    if 'league_table' not in st.session_state:
        st.session_state.league_table = {
            'Team A': {'matches_played': 0, 'points': 0, 'goals_scored': 0, 'wins': 0, 'losses': 0, 'draws': 0},
            'Team B': {'matches_played': 0, 'points': 0, 'goals_scored': 0, 'wins': 0, 'losses': 0, 'draws': 0},
            'Team C': {'matches_played': 0, 'points': 0, 'goals_scored': 0, 'wins': 0, 'losses': 0, 'draws': 0},
            'Team D': {'matches_played': 0, 'points': 0, 'goals_scored': 0, 'wins': 0, 'losses': 0, 'draws': 0}
        }

    if 'player_stats' not in st.session_state:
        st.session_state.player_stats = {}
        for team, players in st.session_state.teams.items():
            for player in players:
                st.session_state.player_stats[player] = {'goals': 0, 'assists': 0, 'team': team}

def update_league_table(home_team, away_team, home_score, away_score):
    # Update matches played
    st.session_state.league_table[home_team]['matches_played'] += 1
    st.session_state.league_table[away_team]['matches_played'] += 1

    # Update goals scored
    st.session_state.league_table[home_team]['goals_scored'] += home_score
    st.session_state.league_table[away_team]['goals_scored'] += away_score

    # Determine winner and update points
    if home_score > away_score:
        # Home team wins
        st.session_state.league_table[home_team]['points'] += 3
        st.session_state.league_table[home_team]['wins'] += 1
        st.session_state.league_table[away_team]['losses'] += 1
    elif away_score > home_score:
        # Away team wins
        st.session_state.league_table[away_team]['points'] += 3
        st.session_state.league_table[away_team]['wins'] += 1
        st.session_state.league_table[home_team]['losses'] += 1
    else:
        # Draw
        st.session_state.league_table[home_team]['points'] += 1
        st.session_state.league_table[away_team]['points'] += 1
        st.session_state.league_table[home_team]['draws'] += 1
        st.session_state.league_table[away_team]['draws'] += 1

def update_player_stats(scorers_data, assists_data):
    for scorer_info in scorers_data:
        if scorer_info['player'] != 'None':
            st.session_state.player_stats[scorer_info['player']]['goals'] += 1

    for assist_info in assists_data:
        if assist_info['player'] != 'None':
            st.session_state.player_stats[assist_info['player']]['assists'] += 1

def clear_all_data():
    st.session_state.matches = []
    st.session_state.league_table = {
        'Team A': {'matches_played': 0, 'points': 0, 'goals_scored': 0, 'wins': 0, 'losses': 0, 'draws': 0},
        'Team B': {'matches_played': 0, 'points': 0, 'goals_scored': 0, 'wins': 0, 'losses': 0, 'draws': 0},
        'Team C': {'matches_played': 0, 'points': 0, 'goals_scored': 0, 'wins': 0, 'losses': 0, 'draws': 0},
        'Team D': {'matches_played': 0, 'points': 0, 'goals_scored': 0, 'wins': 0, 'losses': 0, 'draws': 0}
    }
    for team, players in st.session_state.teams.items():
        for player in players:
            st.session_state.player_stats[player] = {'goals': 0, 'assists': 0, 'team': team}

def main():
    st.set_page_config(page_title="Football League Manager", layout="wide")

    initialize_session_state()

    st.title("⚽ Football League Manager")
    st.markdown("---")

    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📅 Matches", "🏆 League Table", "⚽ Top Scorers", "🎯 Top Assists", "⚙️ Settings"])

    # Tab 1: Matches
    with tab1:
        st.header("Match Management")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Schedule New Match")
            
            teams = list(st.session_state.teams.keys())
            
            col1a, col1b = st.columns(2)
            with col1a:
                home_team = st.selectbox("Home Team", teams, key="home_team")
            with col1b:
                available_away_teams = [team for team in teams if team != home_team]
                away_team = st.selectbox("Away Team", available_away_teams, key="away_team")
            
            match_date = st.date_input("Match Date", value=datetime.now().date())
            
            col2a, col2b = st.columns(2)
            with col2a:
                home_score = st.number_input(f"{home_team} Score", min_value=0, value=0, step=1)
            with col2b:
                away_score = st.number_input(f"{away_team} Score", min_value=0, value=0, step=1)
            
            # Scorers section
            st.subheader("Goal Scorers")
            total_goals = home_score + away_score
            
            scorers_data = []
            assists_data = []
            
            if total_goals > 0:
                for i in range(total_goals):
                    st.write(f"**Goal {i+1}:**")
                    col3a, col3b, col3c = st.columns(3)
                    
                    with col3a:
                        # Determine which teams can score this goal
                        if i < home_score:
                            scoring_team = home_team
                        else:
                            scoring_team = away_team
                        
                        scorer = st.selectbox(
                            f"Scorer",
                            ['None'] + st.session_state.teams[scoring_team],
                            key=f"scorer_{i}"
                        )
                        scorers_data.append({'player': scorer, 'team': scoring_team})
                    
                    with col3b:
                        assist_player = st.selectbox(
                            f"Assist",
                            ['None'] + st.session_state.teams[scoring_team],
                            key=f"assist_{i}"
                        )
                        assists_data.append({'player': assist_player, 'team': scoring_team})
            
            if st.button("Complete Match", type="primary"):
                # Create match record
                match_record = {
                    'date': match_date.strftime("%Y-%m-%d"),
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_score': home_score,
                    'away_score': away_score,
                    'scorers': scorers_data,
                    'assists': assists_data,
                    'completed': True
                }
                
                # Update league table
                update_league_table(home_team, away_team, home_score, away_score)
                
                # Update player statistics
                update_player_stats(scorers_data, assists_data)
                
                # Add match to history
                st.session_state.matches.append(match_record)
                
                st.success(f"Match completed! {home_team} {home_score} - {away_score} {away_team}")
                st.rerun()
        
        with col2:
            st.subheader("Recent Matches")
            if st.session_state.matches:
                for match in reversed(st.session_state.matches[-5:]):  # Show last 5 matches
                    with st.container():
                        st.write(f"**{match['date']}**")
                        st.write(f"{match['home_team']} {match['home_score']} - {match['away_score']} {match['away_team']}")
                        st.write("---")
            else:
                st.write("No matches played yet.")

    # Tab 2: League Table
    with tab2:
        st.header("League Table")
        
        # Convert league table to DataFrame for display
        table_data = []
        for team, stats in st.session_state.league_table.items():
            table_data.append({
                'Team': team,
                'Matches Played': stats['matches_played'],
                'Points': stats['points'],
                'Goals Scored': stats['goals_scored'],
                'Wins': stats['wins'],
                'Draws': stats['draws'],
                'Losses': stats['losses']
            })
        
        df_table = pd.DataFrame(table_data)
        
        # Sort by points (descending), then by goals scored (descending)
        df_table = df_table.sort_values(['Points', 'Goals Scored'], ascending=[False, False]).reset_index(drop=True)
        df_table.index += 1  # Start index from 1
        
        st.dataframe(df_table, use_container_width=True)

    # Tab 3: Top Scorers
    with tab3:
        st.header("Top Scorers")
        
        # Create top scorers dataframe
        scorers_data = []
        for player, stats in st.session_state.player_stats.items():
            if stats['goals'] > 0:
                scorers_data.append({
                    'Player': player,
                    'Team': stats['team'],
                    'Goals': stats['goals']
                })
        
        if scorers_data:
            df_scorers = pd.DataFrame(scorers_data)
            df_scorers = df_scorers.sort_values('Goals', ascending=False).reset_index(drop=True)
            df_scorers.index += 1
            st.dataframe(df_scorers, use_container_width=True)
        else:
            st.write("No goals scored yet.")

    # Tab 4: Top Assists
    with tab4:
        st.header("Top Assists")
        
        # Create top assists dataframe
        assists_data = []
        for player, stats in st.session_state.player_stats.items():
            if stats['assists'] > 0:
                assists_data.append({
                    'Player': player,
                    'Team': stats['team'],
                    'Assists': stats['assists']
                })
        
        if assists_data:
            df_assists = pd.DataFrame(assists_data)
            df_assists = df_assists.sort_values('Assists', ascending=False).reset_index(drop=True)
            df_assists.index += 1
            st.dataframe(df_assists, use_container_width=True)
        else:
            st.write("No assists recorded yet.")

    # Tab 5: Settings
    with tab5:
        st.header("Settings")
        
        st.subheader("Team Management")
        
        # Edit team rosters
        for team_name in st.session_state.teams.keys():
            with st.expander(f"Edit {team_name} Roster"):
                current_players = st.session_state.teams[team_name].copy()
                
                # Display current players with option to remove
                for i, player in enumerate(current_players):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"{i+1}. {player}")
                    with col2:
                        if st.button(f"Remove", key=f"remove_{team_name}_{player}"):
                            st.session_state.teams[team_name].remove(player)
                            if player in st.session_state.player_stats:
                                del st.session_state.player_stats[player]
                            st.rerun()
                
                # Add new player
                new_player = st.text_input(f"Add new player to {team_name}", key=f"new_player_{team_name}")
                if st.button(f"Add Player", key=f"add_{team_name}") and new_player:
                    if new_player not in st.session_state.teams[team_name]:
                        st.session_state.teams[team_name].append(new_player)
                        st.session_state.player_stats[new_player] = {'goals': 0, 'assists': 0, 'team': team_name}
                        st.success(f"Added {new_player} to {team_name}")
                        st.rerun()
                    else:
                        st.error(f"{new_player} already exists in {team_name}")
        
        st.markdown("---")
        
        st.subheader("Reset Data")
        st.warning("⚠️ This will permanently delete all match data, statistics, and reset the league table!")
        
        if st.button("🗑️ Clear All Data", type="secondary"):
            if st.button("⚠️ Confirm - Clear All Data", type="primary"):
                clear_all_data()
                st.success("All data has been cleared!")
                st.rerun()

if __name__ == "__main__":
    main()