import streamlit as st
import random
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Rock Paper Scissors ✂️",
    page_icon="✂️",
    layout="wide"
)

# Custom CSS for game styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF6B35;
        font-size: 4rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 3px 3px 6px rgba(0,0,0,0.3), 0 0 20px #FF6B35; }
        to { text-shadow: 3px 3px 6px rgba(0,0,0,0.3), 0 0 30px #FF6B35, 0 0 40px #FF6B35; }
    }
    
    .game-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        margin: 2rem 0;
        color: white;
        text-align: center;
    }
    
    .choice-button {
        background: white;
        border: 4px solid #FF6B35;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        font-size: 4rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        min-height: 200px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .choice-button:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border-color: #E55100;
        background: #fff8f5;
    }
    
    .choice-selected {
        background: linear-gradient(45deg, #FF6B35, #FF8A65) !important;
        color: white !important;
        border-color: #BF360C !important;
        transform: scale(1.1);
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1.1); }
        50% { transform: scale(1.15); }
        100% { transform: scale(1.1); }
    }
    
    .computer-choice {
        background: linear-gradient(45deg, #2196F3, #64B5F6) !important;
        color: white !important;
        border-color: #0D47A1 !important;
        animation: computerPulse 1s infinite;
    }
    
    @keyframes computerPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .battle-arena {
        background: white;
        border: 3px solid #FF6B35;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    .vs-text {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B35;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    .result-winner {
        background: linear-gradient(45deg, #4CAF50, #81C784);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        animation: celebration 1s ease-in-out;
        margin: 1rem 0;
    }
    
    .result-loser {
        background: linear-gradient(45deg, #F44336, #EF5350);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        animation: shake 0.8s ease-in-out;
        margin: 1rem 0;
    }
    
    .result-draw {
        background: linear-gradient(45deg, #FF9800, #FFB74D);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        animation: wobble 1s ease-in-out;
        margin: 1rem 0;
    }
    
    @keyframes celebration {
        0%, 100% { transform: scale(1) rotate(0deg); }
        25% { transform: scale(1.1) rotate(2deg); }
        75% { transform: scale(1.1) rotate(-2deg); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    @keyframes wobble {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(1deg); }
        75% { transform: rotate(-1deg); }
    }
    
    .score-card {
        background: white;
        border: 3px solid #2196F3;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .score-card:hover {
        transform: translateY(-5px);
    }
    
    .score-number {
        font-size: 3rem;
        font-weight: bold;
        color: #2196F3;
        margin: 0.5rem 0;
    }
    
    .player-wins {
        border-color: #4CAF50 !important;
    }
    
    .player-wins .score-number {
        color: #4CAF50 !important;
    }
    
    .computer-wins {
        border-color: #F44336 !important;
    }
    
    .computer-wins .score-number {
        color: #F44336 !important;
    }
    
    .countdown {
        font-size: 5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        animation: countdownPulse 1s ease-in-out;
    }
    
    @keyframes countdownPulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.2); opacity: 0.7; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .game-stats {
        background: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .emoji-large {
        font-size: 5rem;
        margin: 1rem;
        display: inline-block;
    }
    
    .round-info {
        background: linear-gradient(45deg, #E3F2FD, #BBDEFB);
        border: 2px solid #2196F3;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        color: #0D47A1;
    }
    
    .streak-indicator {
        background: linear-gradient(45deg, #FFF3E0, #FFE0B2);
        border: 2px solid #FF9800;
        border-radius: 10px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        text-align: center;
        font-weight: bold;
        color: #E65100;
    }
</style>
""", unsafe_allow_html=True)

# Game choices with emojis
CHOICES = {
    'rock': {'emoji': '🗿', 'name': 'Rock', 'beats': 'scissors'},
    'paper': {'emoji': '📄', 'name': 'Paper', 'beats': 'rock'},
    'scissors': {'emoji': '✂️', 'name': 'Scissors', 'beats': 'paper'}
}

# Initialize session state
def init_session_state():
    if 'player_score' not in st.session_state:
        st.session_state.player_score = 0
    if 'computer_score' not in st.session_state:
        st.session_state.computer_score = 0
    if 'draws' not in st.session_state:
        st.session_state.draws = 0
    if 'total_games' not in st.session_state:
        st.session_state.total_games = 0
    if 'current_round' not in st.session_state:
        st.session_state.current_round = 0
    if 'player_choice' not in st.session_state:
        st.session_state.player_choice = None
    if 'computer_choice' not in st.session_state:
        st.session_state.computer_choice = None
    if 'game_result' not in st.session_state:
        st.session_state.game_result = None
    if 'show_result' not in st.session_state:
        st.session_state.show_result = False
    if 'game_history' not in st.session_state:
        st.session_state.game_history = []
    if 'win_streak' not in st.session_state:
        st.session_state.win_streak = 0
    if 'best_streak' not in st.session_state:
        st.session_state.best_streak = 0
    if 'computer_streak' not in st.session_state:
        st.session_state.computer_streak = 0

def get_computer_choice():
    """Get computer's random choice"""
    return random.choice(list(CHOICES.keys()))

def determine_winner(player_choice, computer_choice):
    """Determine the winner of the round"""
    if player_choice == computer_choice:
        return 'draw'
    elif CHOICES[player_choice]['beats'] == computer_choice:
        return 'player'
    else:
        return 'computer'

def update_scores(result):
    """Update game scores and statistics"""
    st.session_state.total_games += 1
    st.session_state.current_round += 1
    
    if result == 'player':
        st.session_state.player_score += 1
        st.session_state.win_streak += 1
        st.session_state.computer_streak = 0
        
        if st.session_state.win_streak > st.session_state.best_streak:
            st.session_state.best_streak = st.session_state.win_streak
            
    elif result == 'computer':
        st.session_state.computer_score += 1
        st.session_state.computer_streak += 1
        st.session_state.win_streak = 0
    else:  # draw
        st.session_state.draws += 1

def save_game_to_history(player_choice, computer_choice, result):
    """Save current game to history"""
    st.session_state.game_history.append({
        'round': st.session_state.current_round,
        'player_choice': player_choice,
        'computer_choice': computer_choice,
        'result': result,
        'timestamp': datetime.now(),
        'player_score_after': st.session_state.player_score,
        'computer_score_after': st.session_state.computer_score
    })
    
    # Keep only last 50 games
    if len(st.session_state.game_history) > 50:
        st.session_state.game_history = st.session_state.game_history[-50:]

def reset_game():
    """Reset all game statistics"""
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.draws = 0
    st.session_state.total_games = 0
    st.session_state.current_round = 0
    st.session_state.player_choice = None
    st.session_state.computer_choice = None
    st.session_state.game_result = None
    st.session_state.show_result = False
    st.session_state.game_history = []
    st.session_state.win_streak = 0
    st.session_state.best_streak = 0
    st.session_state.computer_streak = 0

def play_round(player_choice):
    """Play a round of the game"""
    computer_choice = get_computer_choice()
    result = determine_winner(player_choice, computer_choice)
    
    st.session_state.player_choice = player_choice
    st.session_state.computer_choice = computer_choice
    st.session_state.game_result = result
    st.session_state.show_result = True
    
    update_scores(result)
    save_game_to_history(player_choice, computer_choice, result)

# Initialize session state
init_session_state()

# Main header
st.markdown('<h1 class="main-header">🗿📄✂️ ROCK PAPER SCISSORS ✂️📄🗿</h1>', unsafe_allow_html=True)

# Game status and round info
col_status1, col_status2, col_status3 = st.columns(3)

with col_status1:
    st.markdown(f"""
    <div class="round-info">
        🎯 Round: {st.session_state.current_round}
    </div>
    """, unsafe_allow_html=True)

with col_status2:
    st.markdown(f"""
    <div class="round-info">
        🎮 Total Games: {st.session_state.total_games}
    </div>
    """, unsafe_allow_html=True)

with col_status3:
    if st.session_state.win_streak > 0:
        st.markdown(f"""
        <div class="streak-indicator">
            🔥 Win Streak: {st.session_state.win_streak}
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.computer_streak > 0:
        st.markdown(f"""
        <div class="streak-indicator">
            🤖 Computer Streak: {st.session_state.computer_streak}
        </div>
        """, unsafe_allow_html=True)

# Score display
st.markdown("### 🏆 Current Score")

col_score1, col_score2, col_score3 = st.columns(3)

with col_score1:
    score_class = "score-card player-wins" if st.session_state.player_score > st.session_state.computer_score else "score-card"
    st.markdown(f"""
    <div class="{score_class}">
        <div style="font-size: 2rem;">👤 You</div>
        <div class="score-number">{st.session_state.player_score}</div>
        <div style="font-size: 1rem;">Wins</div>
    </div>
    """, unsafe_allow_html=True)

with col_score2:
    st.markdown(f"""
    <div class="score-card">
        <div style="font-size: 2rem;">🤝 Draws</div>
        <div class="score-number">{st.session_state.draws}</div>
        <div style="font-size: 1rem;">Games</div>
    </div>
    """, unsafe_allow_html=True)

with col_score3:
    score_class = "score-card computer-wins" if st.session_state.computer_score > st.session_state.player_score else "score-card"
    st.markdown(f"""
    <div class="{score_class}">
        <div style="font-size: 2rem;">🤖 Computer</div>
        <div class="score-number">{st.session_state.computer_score}</div>
        <div style="font-size: 1rem;">Wins</div>
    </div>
    """, unsafe_allow_html=True)

# Game area
st.markdown("---")

if not st.session_state.show_result:
    # Choice selection phase
    st.markdown("### 🎯 Choose Your Weapon!")
    
    col_choice1, col_choice2, col_choice3 = st.columns(3)
    
    with col_choice1:
        if st.button("🗿\n**ROCK**", key="rock_btn", use_container_width=True):
            play_round('rock')
            st.rerun()
    
    with col_choice2:
        if st.button("📄\n**PAPER**", key="paper_btn", use_container_width=True):
            play_round('paper')
            st.rerun()
    
    with col_choice3:
        if st.button("✂️\n**SCISSORS**", key="scissors_btn", use_container_width=True):
            play_round('scissors')
            st.rerun()

else:
    # Result display phase
    st.markdown("### ⚔️ Battle Result!")
    
    # Battle arena
    st.markdown(f"""
    <div class="battle-arena">
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 2rem 0;">
            <div style="text-align: center; flex: 1;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">👤 YOU</div>
                <div class="emoji-large">{CHOICES[st.session_state.player_choice]['emoji']}</div>
                <div style="font-size: 1.5rem; font-weight: bold; color: #2196F3;">
                    {CHOICES[st.session_state.player_choice]['name']}
                </div>
            </div>
            
            <div class="vs-text" style="flex: 0.5;">VS</div>
            
            <div style="text-align: center; flex: 1;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">🤖 COMPUTER</div>
                <div class="emoji-large">{CHOICES[st.session_state.computer_choice]['emoji']}</div>
                <div style="font-size: 1.5rem; font-weight: bold; color: #F44336;">
                    {CHOICES[st.session_state.computer_choice]['name']}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Result announcement
    if st.session_state.game_result == 'player':
        result_class = "result-winner"
        result_text = "🎉 YOU WIN! 🎉"
        explanation = f"{CHOICES[st.session_state.player_choice]['name']} beats {CHOICES[st.session_state.computer_choice]['name']}!"
    elif st.session_state.game_result == 'computer':
        result_class = "result-loser"
        result_text = "😔 COMPUTER WINS! 😔"
        explanation = f"{CHOICES[st.session_state.computer_choice]['name']} beats {CHOICES[st.session_state.player_choice]['name']}!"
    else:  # draw
        result_class = "result-draw"
        result_text = "🤝 IT'S A DRAW! 🤝"
        explanation = "Both chose the same thing!"
    
    st.markdown(f"""
    <div class="{result_class}">
        {result_text}
        <div style="font-size: 1.2rem; margin-top: 1rem; opacity: 0.9;">
            {explanation}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col_action1, col_action2 = st.columns(2)
    
    with col_action1:
        if st.button("🔄 Play Again", use_container_width=True, type="primary"):
            st.session_state.show_result = False
            st.rerun()
    
    with col_action2:
        if st.button("📊 View Stats", use_container_width=True):
            st.session_state.show_result = False
            # Will show stats section below

# Game controls
st.markdown("---")
st.markdown("### 🎮 Game Controls")

col_control1, col_control2, col_control3 = st.columns(3)

with col_control1:
    if st.button("🆕 New Game", use_container_width=True, type="secondary"):
        reset_game()
        st.success("New game started!")
        st.rerun()

with col_control2:
    if st.button("🔄 Continue Playing", use_container_width=True):
        st.session_state.show_result = False
        st.rerun()

with col_control3:
    # Auto-play option
    if st.button("🎲 Random Round", use_container_width=True):
        random_choice = random.choice(list(CHOICES.keys()))
        play_round(random_choice)
        st.rerun()

# Statistics section
if st.session_state.total_games > 0:
    st.markdown("---")
    st.markdown("### 📊 Game Statistics")
    
    # Overall statistics
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        win_rate = (st.session_state.player_score / st.session_state.total_games) * 100
        st.metric("Win Rate", f"{win_rate:.1f}%")
    
    with col_stat2:
        st.metric("Best Streak", st.session_state.best_streak)
    
    with col_stat3:
        if st.session_state.total_games > 0:
            draw_rate = (st.session_state.draws / st.session_state.total_games) * 100
            st.metric("Draw Rate", f"{draw_rate:.1f}%")
    
    with col_stat4:
        computer_win_rate = (st.session_state.computer_score / st.session_state.total_games) * 100
        st.metric("Computer Win Rate", f"{computer_win_rate:.1f}%")
    
    # Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Results distribution
        results_data = {
            'Result': ['👤 Your Wins', '🤖 Computer Wins', '🤝 Draws'],
            'Count': [st.session_state.player_score, st.session_state.computer_score, st.session_state.draws],
            'Color': ['#4CAF50', '#F44336', '#FF9800']
        }
        
        results_df = pd.DataFrame(results_data)
        results_df = results_df[results_df['Count'] > 0]  # Only show non-zero values
        
        if not results_df.empty:
            fig_results = px.pie(
                results_df, 
                values='Count', 
                names='Result',
                title='Game Results Distribution',
                color_discrete_sequence=['#4CAF50', '#F44336', '#FF9800']
            )
            fig_results.update_layout(height=400)
            st.plotly_chart(fig_results, use_container_width=True)
    
    with col_chart2:
        # Choice frequency analysis
        if st.session_state.game_history:
            choice_counts = {}
            computer_choice_counts = {}
            
            for game in st.session_state.game_history:
                player_choice = game['player_choice']
                computer_choice = game['computer_choice']
                
                choice_counts[player_choice] = choice_counts.get(player_choice, 0) + 1
                computer_choice_counts[computer_choice] = computer_choice_counts.get(computer_choice, 0) + 1
            
            if choice_counts:
                choice_data = []
                for choice, count in choice_counts.items():
                    choice_data.append({
                        'Choice': f"{CHOICES[choice]['emoji']} {CHOICES[choice]['name']}",
                        'Your Count': count,
                        'Computer Count': computer_choice_counts.get(choice, 0)
                    })
                
                choice_df = pd.DataFrame(choice_data)
                
                fig_choices = px.bar(
                    choice_df, 
                    x='Choice', 
                    y=['Your Count', 'Computer Count'],
                    title='Choice Frequency Comparison',
                    barmode='group'
                )
                fig_choices.update_layout(height=400)
                st.plotly_chart(fig_choices, use_container_width=True)
    
    # Performance trend
    if len(st.session_state.game_history) >= 5:
        st.markdown("### 📈 Performance Trend (Last 20 Games)")
        
        recent_games = st.session_state.game_history[-20:]
        trend_data = []
        cumulative_wins = 0
        
        for i, game in enumerate(recent_games):
            if game['result'] == 'player':
                cumulative_wins += 1
            
            win_rate_at_game = (cumulative_wins / (i + 1)) * 100
            trend_data.append({
                'Game': i + 1,
                'Win Rate': win_rate_at_game,
                'Result': '🎉 Win' if game['result'] == 'player' else ('🤝 Draw' if game['result'] == 'draw' else '😔 Loss')
            })
        
        trend_df = pd.DataFrame(trend_data)
        
        fig_trend = px.line(
            trend_df,
            x='Game',
            y='Win Rate',
            title='Win Rate Trend',
            markers=True
        )
        fig_trend.update_layout(height=400, yaxis_title='Win Rate (%)', xaxis_title='Recent Games')
        st.plotly_chart(fig_trend, use_container_width=True)

# Recent game history
if st.session_state.game_history:
    st.markdown("---")
    st.markdown("### 📜 Recent Games")
    
    # Show last 10 games
    recent_games = list(reversed(st.session_state.game_history[-10:]))
    
    for game in recent_games:
        result_emoji = '🎉' if game['result'] == 'player' else ('🤝' if game['result'] == 'draw' else '😔')
        result_text = 'WIN' if game['result'] == 'player' else ('DRAW' if game['result'] == 'draw' else 'LOSS')
        
        col_game1, col_game2, col_game3, col_game4 = st.columns([1, 2, 2, 1])
        
        with col_game1:
            st.markdown(f"**Round {game['round']}**")
        
        with col_game2:
            st.markdown(f"👤 {CHOICES[game['player_choice']]['emoji']} vs 🤖 {CHOICES[game['computer_choice']]['emoji']}")
        
        with col_game3:
            st.markdown(f"{CHOICES[game['player_choice']]['name']} vs {CHOICES[game['computer_choice']]['name']}")
        
        with col_game4:
            st.markdown(f"{result_emoji} **{result_text}**")

# Game rules and tips
st.markdown("---")
st.markdown("### 📚 How to Play & Strategy Tips")

col_rules1, col_rules2, col_rules3 = st.columns(3)

with col_rules1:
    st.markdown("""
    #### 📖 Rules
    - 🗿 **Rock** crushes ✂️ **Scissors**
    - 📄 **Paper** covers 🗿 **Rock**  
    - ✂️ **Scissors** cuts 📄 **Paper**
    - Same choice = Draw
    """)

with col_rules2:
    st.markdown("""
    #### 💡 Strategy Tips
    - 🧠 Look for computer patterns
    - 🎲 Mix up your choices
    - 📊 Use statistics to your advantage
    - 🔥 Build winning streaks
    """)

with col_rules3:
    st.markdown("""
    #### 🏆 Achievements
    - 🎯 Win Rate > 60%
    - 🔥 Win Streak ≥ 5
    - 🎮 Play 100+ games
    - ⚖️ Master of balance
    """)

# Footer
st.markdown(
    """
    <div style='text-align: center; margin-top: 3rem; padding: 2rem; background: linear-gradient(45deg, #FF6B35, #FF8A65); border-radius: 15px;'>
    <h4 style='color: white; margin: 0;'>🗿📄✂️ "In the battle of choices, strategy wins!" ✂️📄🗿</h4>
    <p style='color: white; margin: 0.5rem 0 0 0;'>Challenge the computer and prove your rock-paper-scissors mastery!</p>
    </div>
    """,
    unsafe_allow_html=True
)