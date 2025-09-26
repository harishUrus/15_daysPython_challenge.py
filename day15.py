import streamlit as st
import random
import time

# --- Game Configuration ---
# Set page configuration for a wider layout
st.set_page_config(layout="wide")

# Define grid size and cell size for rendering
GRID_SIZE = 20
CELL_SIZE = 20

# Define colors for the game elements using a CSS-like style
COLORS = {
    "background": "#2c3e50",  # Dark blue-gray
    "snake_head": "#27ae60",  # Emerald green
    "snake_body": "#2ecc71",  # Brighter green
    "food": "#e74c3c",        # Red
    "wall": "#34495e"         # Darker blue-gray
}

# --- Session State Initialization ---
# This ensures the game state persists across reruns
if 'game_over' not in st.session_state:
    st.session_state.game_over = True
    # Initialize all game-related state variables here to prevent errors on the first run
    st.session_state.score = 0
    st.session_state.snake = [(GRID_SIZE // 2, GRID_SIZE // 2)]
    st.session_state.direction = "Right"
    st.session_state.food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    st.session_state.speed = 0.2

def initialize_game():
    """Initializes or resets the game state."""
    st.session_state.game_over = False
    st.session_state.score = 0
    # The snake starts in the center of the grid
    st.session_state.snake = [(GRID_SIZE // 2, GRID_SIZE // 2)]
    st.session_state.direction = "Right"
    # Generate the first food item
    generate_food()
    st.session_state.speed = 0.2  # Initial speed

def generate_food():
    """Generates a new random position for the food."""
    while True:
        food_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        # Ensure food does not appear on the snake's body
        if food_pos not in st.session_state.snake:
            st.session_state.food = food_pos
            break

def check_collision():
    """Checks for collisions with walls or the snake's own body."""
    head_x, head_y = st.session_state.snake[0]
    
    # Check for wall collision
    if head_x < 0 or head_x >= GRID_SIZE or head_y < 0 or head_y >= GRID_SIZE:
        st.session_state.game_over = True
        return True
    
    # Check for self-collision
    if st.session_state.snake[0] in st.session_state.snake[1:]:
        st.session_state.game_over = True
        return True
        
    return False

def update_game():
    """Updates the game state for the next frame."""
    head_x, head_y = st.session_state.snake[0]
    direction = st.session_state.direction
    
    new_head = (head_x, head_y)
    if direction == "Up":
        new_head = (head_x, head_y - 1)
    elif direction == "Down":
        new_head = (head_x, head_y + 1)
    elif direction == "Left":
        new_head = (head_x - 1, head_y)
    elif direction == "Right":
        new_head = (head_x + 1, head_y)
        
    # Add the new head to the snake
    st.session_state.snake.insert(0, new_head)
    
    # Check if the snake ate the food
    if st.session_state.snake[0] == st.session_state.food:
        st.session_state.score += 1
        # Increase speed slightly for more challenge
        if st.session_state.speed > 0.05:
            st.session_state.speed -= 0.005
        generate_food()
    else:
        # Remove the tail to simulate movement
        st.session_state.snake.pop()
        
    # Check for collision after moving the snake
    check_collision()

def draw_board():
    """
    Renders the game board using a combination of Streamlit markdown and CSS.
    Each cell is represented by a small colored box.
    """
    board_html = f"""
    <div style="
        display: grid; 
        grid-template-columns: repeat({GRID_SIZE}, {CELL_SIZE}px);
        grid-template-rows: repeat({GRID_SIZE}, {CELL_SIZE}px);
        width: {GRID_SIZE * CELL_SIZE}px;
        height: {GRID_SIZE * CELL_SIZE}px;
        background-color: {COLORS['background']};
        border-radius: 10px;
        overflow: hidden;
    ">
    """
    
    # Draw each cell of the grid
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = ""
            if (x, y) == st.session_state.food:
                color = COLORS['food']
            elif (x, y) == st.session_state.snake[0]:
                color = COLORS['snake_head']
            elif (x, y) in st.session_state.snake:
                color = COLORS['snake_body']

            if color:
                board_html += f"""
                <div style="
                    background-color: {color};
                    border-radius: 3px;
                    margin: 1px;
                "></div>
                """
            else:
                board_html += f"<div></div>"
                
    board_html += "</div>"
    st.markdown(board_html, unsafe_allow_html=True)

# --- Streamlit UI ---
st.title("🐍 Classic Snake Game")

col1, col2 = st.columns([1, 1])

# Sidebar for controls and score
with col1:
    st.subheader("Controls")
    
    # Using columns for a cleaner button layout
    button_col1, button_col2, button_col3 = st.columns([1, 1, 1])

    with button_col2:
        if st.button("Up", use_container_width=True):
            if st.session_state.direction != "Down":
                st.session_state.direction = "Up"
    
    button_col1, button_col2, button_col3 = st.columns([1, 1, 1])
    with button_col1:
        if st.button("Left", use_container_width=True):
            if st.session_state.direction != "Right":
                st.session_state.direction = "Left"
    with button_col3:
        if st.button("Right", use_container_width=True):
            if st.session_state.direction != "Left":
                st.session_state.direction = "Right"

    button_col1, button_col2, button_col3 = st.columns([1, 1, 1])
    with button_col2:
        if st.button("Down", use_container_width=True):
            if st.session_state.direction != "Up":
                st.session_state.direction = "Down"

    st.markdown("---")
    st.subheader(f"Score: {st.session_state.score}")
    
    if st.button("Start New Game"):
        initialize_game()
        
    st.markdown("---")
    if st.session_state.game_over:
        st.error("Game Over!")

# Main game board display
with col2:
    game_board_placeholder = st.empty()

# --- Game Loop ---
# This loop runs continuously to update the game
if not st.session_state.game_over:
    with game_board_placeholder:
        draw_board()
    
    update_game()
    time.sleep(st.session_state.speed)
    st.rerun()
    
# Initial display when the game is over
if st.session_state.game_over:
    with game_board_placeholder:
        st.markdown(
            f"""
            <div style="
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                width: {GRID_SIZE * CELL_SIZE}px;
                height: {GRID_SIZE * CELL_SIZE}px;
                background-color: {COLORS['background']};
                border-radius: 10px;
                color: white;
                font-size: 2em;
                text-align: center;
            ">
            <h1>Game Over!</h1>
            <h2>Final Score: {st.session_state.score}</h2>
            </div>
            """, unsafe_allow_html=True
        )
