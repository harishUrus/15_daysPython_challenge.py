import streamlit as st
import random
import time
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Tic-Tac-Toe Game ❌⭕",
    page_icon="⭕",
    layout="wide"
)

# Custom CSS for game styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 4rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    }
    
    .game-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        margin: 2rem 0;
        color: white;
        text-align: center;
    }
    
    .game-board {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        max-width: 400px;
        margin: 2rem auto;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .cell-button {
        aspect-ratio: 1;
        font-size: 3rem;
        font-weight: bold;
        border: 3px solid #2E86AB;
        border-radius: 12px;
        background: #f8f9fa;
        color: #2E86AB;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .cell-button:hover {
        background: #e3f2fd;
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .cell-x {
        color: #E74C3C;
        background: #ffebee;
        border-color: #E74C3C;
    }
    
    .cell-o {
        color: #2E86AB;
        background: #e3f2fd;
        border-color: #2E86AB;
    }
    
    .winning-cell {
        background: linear-gradient(45deg, #4CAF50, #81C784) !important;
        color: white !important;
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .game-status {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .status-playing {
        background: linear-gradient(45deg, #FF9800, #FFB74D);
        color: white;
    }
    
    .status-winner {
        background: linear-gradient(45deg, #4CAF50, #81C784);
        color: white;
        animation: celebration 2s ease-in-out;
    }
    
    .status-draw {
        background: linear-gradient(45deg, #9E9E9E, #BDBDBD);
        color: white;
    }
    
    @keyframes celebration {
        0%, 100% { transform: scale(1); }
        25% { transform: scale(1.1) rotate(2deg); }
        75% { transform: scale(1.1) rotate(-2deg); }
    }
    
    .player-info {
        background: white;
        border: 3px solid #2E86AB;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .current-player {
        background: linear-gradient(45deg, #2E86AB, #64B5F6);
        color: white;
        transform: scale(1.05);
    }
    
    .stats-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .difficulty-badge {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.25rem;
        display: inline-block;
    }
    
    .easy { background-color: #4CAF50; color: white; }
    .medium { background-color: #FF9800; color: white; }
    .hard { background-color: #F44336; color: white; }
    
    .mode-selector {
        background: white;
        border: 2px solid #2E86AB;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .emoji-large {
        font-size: 4rem;
        margin: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'board' not in st.session_state:
        st.session_state.board = [['' for _ in range(3)] for _ in range(3)]
    if 'current_player' not in st.session_state:
        st.session_state.current_player = 'X'
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'winner' not in st.session_state:
        st.session_state.winner = None
    if 'winning_line' not in st.session_state:
        st.session_state.winning_line = []
    if 'game_mode' not in st.session_state:
        st.session_state.game_mode = 'two_player'
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = 'medium'
    if 'player_names' not in st.session_state:
        st.session_state.player_names = {'X': 'Player 1', 'O': 'Player 2'}
    if 'game_stats' not in st.session_state:
        st.session_state.game_stats = {
            'games_played': 0,
            'x_wins': 0,
            'o_wins': 0,
            'draws': 0,
            'vs_computer_wins': 0,
            'vs_computer_losses': 0
        }
    if 'move_history' not in st.session_state:
        st.session_state.move_history = []

def reset_board():
    """Reset the game board"""
    st.session_state.board = [['' for _ in range(3)] for _ in range(3)]
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.winning_line = []
    st.session_state.move_history = []

def check_winner():
    """Check if there's a winner and return winner and winning line"""
    board = st.session_state.board
    
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0], [(i, 0), (i, 1), (i, 2)]
    
    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != '':
            return board[0][j], [(0, j), (1, j), (2, j)]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2], [(0, 2), (1, 1), (2, 0)]
    
    return None, []

def is_board_full():
    """Check if the board is full"""
    return all(cell != '' for row in st.session_state.board for cell in row)

def get_empty_cells():
    """Get list of empty cells"""
    empty = []
    for i in range(3):
        for j in range(3):
            if st.session_state.board[i][j] == '':
                empty.append((i, j))
    return empty

def computer_move():
    """Make computer move based on difficulty"""
    empty_cells = get_empty_cells()
    
    if not empty_cells:
        return
    
    if st.session_state.difficulty == 'easy':
        # Random move
        move = random.choice(empty_cells)
    
    elif st.session_state.difficulty == 'medium':
        # 70% strategic, 30% random
        if random.random() < 0.7:
            move = get_best_move() or random.choice(empty_cells)
        else:
            move = random.choice(empty_cells)
    
    else:  # hard
        # Always strategic
        move = get_best_move() or random.choice(empty_cells)
    
    if move:
        st.session_state.board[move[0]][move[1]] = st.session_state.current_player
        st.session_state.move_history.append({
            'player': st.session_state.current_player,
            'position': move,
            'move_number': len(st.session_state.move_history) + 1
        })

def get_best_move():
    """Get best strategic move for computer"""
    board = st.session_state.board
    
    # Try to win
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'O'
                winner, _ = check_winner()
                board[i][j] = ''
                if winner == 'O':
                    return (i, j)
    
    # Try to block player from winning
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'X'
                winner, _ = check_winner()
                board[i][j] = ''
                if winner == 'X':
                    return (i, j)
    
    # Take center if available
    if board[1][1] == '':
        return (1, 1)
    
    # Take corners
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    available_corners = [corner for corner in corners if board[corner[0]][corner[1]] == '']
    if available_corners:
        return random.choice(available_corners)
    
    # Take sides
    sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
    available_sides = [side for side in sides if board[side[0]][side[1]] == '']
    if available_sides:
        return random.choice(available_sides)
    
    return None

def make_move(row, col):
    """Make a move on the board"""
    if st.session_state.board[row][col] == '' and not st.session_state.game_over:
        st.session_state.board[row][col] = st.session_state.current_player
        st.session_state.move_history.append({
            'player': st.session_state.current_player,
            'position': (row, col),
            'move_number': len(st.session_state.move_history) + 1
        })
        
        # Check for winner
        winner, winning_line = check_winner()
        
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
            st.session_state.winning_line = winning_line
            update_stats(winner)
        elif is_board_full():
            st.session_state.game_over = True
            st.session_state.winner = 'Draw'
            update_stats('Draw')
        else:
            # Switch players
            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'
            
            # Computer move if in computer mode and it's O's turn
            if (st.session_state.game_mode == 'vs_computer' and 
                st.session_state.current_player == 'O' and 
                not st.session_state.game_over):
                
                time.sleep(0.5)  # Brief pause for better UX
                computer_move()
                
                # Check for winner after computer move
                winner, winning_line = check_winner()
                if winner:
                    st.session_state.game_over = True
                    st.session_state.winner = winner
                    st.session_state.winning_line = winning_line
                    update_stats(winner)
                elif is_board_full():
                    st.session_state.game_over = True
                    st.session_state.winner = 'Draw'
                    update_stats('Draw')
                else:
                    st.session_state.current_player = 'X'

def update_stats(winner):
    """Update game statistics"""
    st.session_state.game_stats['games_played'] += 1
    
    if winner == 'X':
        st.session_state.game_stats['x_wins'] += 1
        if st.session_state.game_mode == 'vs_computer':
            st.session_state.game_stats['vs_computer_wins'] += 1
    elif winner == 'O':
        st.session_state.game_stats['o_wins'] += 1
        if st.session_state.game_mode == 'vs_computer':
            st.session_state.game_stats['vs_computer_losses'] += 1
    else:  # Draw
        st.session_state.game_stats['draws'] += 1

# Initialize session state
init_session_state()

# Main header
st.markdown('<h1 class="main-header">❌⭕ TIC-TAC-TOE GAME ⭕❌</h1>', unsafe_allow_html=True)

# Game setup section
st.markdown("### 🎮 Game Setup")

col_setup1, col_setup2, col_setup3 = st.columns(3)

with col_setup1:
    st.markdown("#### 🎯 Game Mode")
    game_mode = st.radio(
        "Choose mode:",
        ["two_player", "vs_computer"],
        format_func=lambda x: "👥 Two Players" if x == "two_player" else "🤖 vs Computer",
        key="mode_selector"
    )
    st.session_state.game_mode = game_mode

with col_setup2:
    if st.session_state.game_mode == "vs_computer":
        st.markdown("#### ⚙️ Difficulty")
        difficulty = st.radio(
            "Computer difficulty:",
            ["easy", "medium", "hard"],
            format_func=lambda x: f"{'🟢 Easy' if x == 'easy' else '🟡 Medium' if x == 'medium' else '🔴 Hard'}",
            key="difficulty_selector"
        )
        st.session_state.difficulty = difficulty
    else:
        st.markdown("#### 👥 Player Names")
        st.session_state.player_names['X'] = st.text_input("Player X (❌):", value=st.session_state.player_names['X'])
        st.session_state.player_names['O'] = st.text_input("Player O (⭕):", value=st.session_state.player_names['O'])

with col_setup3:
    st.markdown("#### 🎲 Game Controls")
    if st.button("🆕 New Game", use_container_width=True, type="primary"):
        reset_board()
        st.rerun()
    
    if st.button("📊 Reset Stats", use_container_width=True, type="secondary"):
        st.session_state.game_stats = {
            'games_played': 0, 'x_wins': 0, 'o_wins': 0, 'draws': 0,
            'vs_computer_wins': 0, 'vs_computer_losses': 0
        }
        st.success("Statistics reset!")
        st.rerun()

# Main game area
st.markdown("---")

col_game1, col_game2, col_game3 = st.columns([1, 2, 1])

# Left sidebar - Current player info
with col_game1:
    st.markdown("### 👤 Players")
    
    # Player X info
    x_class = "player-info current-player" if st.session_state.current_player == 'X' and not st.session_state.game_over else "player-info"
    st.markdown(f"""
    <div class="{x_class}">
        <h4>❌ {st.session_state.player_names['X']}</h4>
        <p>Wins: {st.session_state.game_stats['x_wins']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Player O info
    o_name = st.session_state.player_names['O'] if st.session_state.game_mode == 'two_player' else '🤖 Computer'
    o_class = "player-info current-player" if st.session_state.current_player == 'O' and not st.session_state.game_over else "player-info"
    st.markdown(f"""
    <div class="{o_class}">
        <h4>⭕ {o_name}</h4>
        <p>Wins: {st.session_state.game_stats['o_wins']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Current game info
    st.markdown("### 📋 Current Game")
    st.markdown(f"**Move:** {len(st.session_state.move_history)}")
    
    if st.session_state.game_mode == 'vs_computer':
        st.markdown(f"**Difficulty:** {st.session_state.difficulty.title()}")

# Center - Game board
with col_game2:
    # Game status
    if st.session_state.game_over:
        if st.session_state.winner == 'Draw':
            status_class = "game-status status-draw"
            status_text = "🤝 IT'S A DRAW! 🤝"
        else:
            status_class = "game-status status-winner"
            winner_name = st.session_state.player_names[st.session_state.winner] if st.session_state.game_mode == 'two_player' and st.session_state.winner in st.session_state.player_names else ('🤖 Computer' if st.session_state.winner == 'O' and st.session_state.game_mode == 'vs_computer' else st.session_state.player_names.get(st.session_state.winner, f'Player {st.session_state.winner}'))
            status_text = f"🎉 {winner_name} WINS! 🎉"
    else:
        status_class = "game-status status-playing"
        current_name = st.session_state.player_names[st.session_state.current_player] if st.session_state.game_mode == 'two_player' else ('🤖 Computer' if st.session_state.current_player == 'O' else st.session_state.player_names['X'])
        status_text = f"🎯 {current_name}'s Turn ({st.session_state.current_player})"
    
    st.markdown(f'<div class="{status_class}">{status_text}</div>', unsafe_allow_html=True)
    
    # Game board
    st.markdown("### 🎯 Game Board")
    
    # Create 3x3 grid of buttons
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            with cols[j]:
                cell_value = st.session_state.board[i][j]
                
                # Determine cell styling
                if (i, j) in st.session_state.winning_line:
                    button_class = "winning-cell"
                elif cell_value == 'X':
                    button_class = "cell-x"
                elif cell_value == 'O':
                    button_class = "cell-o"
                else:
                    button_class = "cell-button"
                
                # Display cell content
                display_value = '❌' if cell_value == 'X' else '⭕' if cell_value == 'O' else ''
                
                if st.button(
                    display_value or '⬜',
                    key=f"cell_{i}_{j}",
                    disabled=st.session_state.game_over or cell_value != '' or (st.session_state.game_mode == 'vs_computer' and st.session_state.current_player == 'O'),
                    use_container_width=True
                ):
                    make_move(i, j)
                    st.rerun()

# Right sidebar - Statistics and move history
with col_game3:
    st.markdown("### 📊 Statistics")
    
    # Game stats
    stats = st.session_state.game_stats
    st.metric("Games Played", stats['games_played'])
    st.metric("Draws", stats['draws'])
    
    if st.session_state.game_mode == 'vs_computer':
        st.metric("Your Wins", stats['vs_computer_wins'])
        st.metric("Computer Wins", stats['vs_computer_losses'])
        
        if stats['games_played'] > 0:
            win_rate = (stats['vs_computer_wins'] / stats['games_played']) * 100
            st.metric("Win Rate", f"{win_rate:.1f}%")
    else:
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("❌ Wins", stats['x_wins'])
        with col_stat2:
            st.metric("⭕ Wins", stats['o_wins'])
    
    # Move history
    if st.session_state.move_history:
        st.markdown("### 📜 Move History")
        
        for move in st.session_state.move_history[-6:]:  # Show last 6 moves
            player_symbol = '❌' if move['player'] == 'X' else '⭕'
            st.markdown(f"**{move['move_number']}.** {player_symbol} → ({move['position'][0]+1},{move['position'][1]+1})")

# Statistics dashboard
if st.session_state.game_stats['games_played'] > 0:
    st.markdown("---")
    st.markdown("### 📈 Game Analytics")
    
    # Create statistics charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Win distribution pie chart
        if st.session_state.game_mode == 'two_player':
            win_data = {
                'Result': ['❌ Player X Wins', '⭕ Player O Wins', '🤝 Draws'],
                'Count': [stats['x_wins'], stats['o_wins'], stats['draws']]
            }
        else:
            win_data = {
                'Result': ['🎯 Your Wins', '🤖 Computer Wins', '🤝 Draws'],
                'Count': [stats['vs_computer_wins'], stats['vs_computer_losses'], stats['draws']]
            }
        
        win_df = pd.DataFrame(win_data)
        win_df = win_df[win_df['Count'] > 0]  # Only show non-zero values
        
        if not win_df.empty:
            fig_wins = px.pie(win_df, values='Count', names='Result', title='Game Results Distribution')
            fig_wins.update_layout(height=400)
            st.plotly_chart(fig_wins, use_container_width=True)
    
    with col_chart2:
        # Performance over time (if enough games)
        if stats['games_played'] >= 5:
            st.markdown("### 🎯 Recent Performance")
            
            # Create sample performance data (in a real app, you'd track this)
            recent_games = min(10, stats['games_played'])
            performance_data = []
            
            for i in range(recent_games):
                # Simulate recent game results based on current stats
                if st.session_state.game_mode == 'vs_computer':
                    win_prob = stats['vs_computer_wins'] / stats['games_played']
                    result = 'Win' if random.random() < win_prob else ('Loss' if random.random() < 0.7 else 'Draw')
                else:
                    x_prob = stats['x_wins'] / stats['games_played']
                    o_prob = stats['o_wins'] / stats['games_played']
                    rand_val = random.random()
                    if rand_val < x_prob:
                        result = 'X Win'
                    elif rand_val < x_prob + o_prob:
                        result = 'O Win'
                    else:
                        result = 'Draw'
                
                performance_data.append({
                    'Game': f'Game {i+1}',
                    'Result': result
                })
            
            perf_df = pd.DataFrame(performance_data)
            result_counts = perf_df['Result'].value_counts()
            
            fig_perf = px.bar(x=result_counts.index, y=result_counts.values, title=f'Last {recent_games} Games')
            fig_perf.update_layout(height=400, xaxis_title='Result', yaxis_title='Count')
            st.plotly_chart(fig_perf, use_container_width=True)
        else:
            st.info("Play at least 5 games to see performance trends!")

# Game tips and rules
st.markdown("---")
st.markdown("### 📚 How to Play & Tips")

col_rules1, col_rules2, col_rules3 = st.columns(3)

with col_rules1:
    st.markdown("""
    #### 📖 Rules
    - Players take turns placing ❌ and ⭕
    - First to get 3 in a row wins
    - Rows, columns, or diagonals count
    - If board fills with no winner, it's a draw
    """)

with col_rules2:
    st.markdown("""
    #### 💡 Strategy Tips
    - Control the center square
    - Block opponent's winning moves
    - Create multiple winning threats
    - Watch for fork opportunities
    """)

with col_rules3:
    st.markdown("""
    #### 🤖 Computer Modes
    - **🟢 Easy:** Random moves
    - **🟡 Medium:** Mix of strategy & random
    - **🔴 Hard:** Always strategic
    """)

# Footer
st.markdown(
    """
    <div style='text-align: center; margin-top: 3rem; padding: 2rem; background: linear-gradient(45deg, #2E86AB, #64B5F6); border-radius: 15px;'>
    <h4 style='color: white; margin: 0;'>❌⭕ "Three in a row, and victory you'll know!" ⭕❌</h4>
    <p style='color: white; margin: 0.5rem 0 0 0;'>Challenge friends or test your skills against our AI!</p>
    </div>
    """,
    unsafe_allow_html=True
)