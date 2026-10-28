
import streamlit as st
import random
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Snake Game",
    page_icon="🐍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Mobile-friendly design
st.markdown("""
<style>
    .block-container {
        max-width: 420px;
        padding: 0.4rem 0.5rem 0.5rem;
    }

    h1 {
        text-align: center;
        font-size: 1.6rem !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    h3 {
        text-align: center;
        margin: 0.2rem 0 !important;
    }

    [data-testid="stMetric"] {
        padding: 0 !important;
        text-align: center;
    }

    div.stButton > button {
        min-height: 42px;
        border-radius: 12px;
        font-size: 18px;
        padding: 0 !important;
    }

    .board {
        display: grid;
        grid-template-columns: repeat(15, minmax(0, 1fr));
        gap: 1px;
        background: #111827;
        border: 2px solid #111827;
        width: min(78vw, 310px);
        margin: 5px auto 8px;
        box-sizing: border-box;
    }

    .cell {
        aspect-ratio: 1;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        line-height: 1;
    }
</style>
""", unsafe_allow_html=True)

SIZE = 15

# Start or restart the game
def new_game():
    st.session_state.snake = [(7, 7), (6, 7), (5, 7)]
    st.session_state.direction = (1, 0)
    st.session_state.food = (10, 7)
    st.session_state.score = 0
    st.session_state.over = False

if "snake" not in st.session_state:
    new_game()

# Change direction without reversing into itself
def turn(new_direction):
    dx, dy = st.session_state.direction
    nx, ny = new_direction

    if (nx, ny) != (-dx, -dy):
        st.session_state.direction = new_direction

# Move the snake more slowly: 500 milliseconds per refresh
if not st.session_state.over:
    st_autorefresh(interval=500, key="game_timer")

    dx, dy = st.session_state.direction
    x, y = st.session_state.snake[0]
    head = (x + dx, y + dy)

    eating = head == st.session_state.food

    # Allow the tail's old position when it moves away
    body = (
        st.session_state.snake
        if eating
        else st.session_state.snake[:-1]
    )

    # Detect wall and body collisions
    if (
        head[0] < 0 or head[0] >= SIZE
        or head[1] < 0 or head[1] >= SIZE
        or head in body
    ):
        st.session_state.over = True

    else:
        st.session_state.snake.insert(0, head)

        if eating:
            st.session_state.score += 1

            empty_cells = [
                (x, y)
                for x in range(SIZE)
                for y in range(SIZE)
                if (x, y) not in st.session_state.snake
            ]

            if empty_cells:
                st.session_state.food = random.choice(empty_cells)
            else:
                st.session_state.over = True
        else:
            st.session_state.snake.pop()

# Title and score
st.title("🐍 Snake Game")
st.metric("🏆 SCORE", st.session_state.score)

# Draw the game board
snake = st.session_state.snake
food = st.session_state.food
cells = []

for y in range(SIZE):
    for x in range(SIZE):
        pos = (x, y)

        if pos == snake[0]:
            color = "#a3e635"
            symbol = "🐍"
        elif pos in snake:
            color = "#22c55e"
            symbol = ""
        elif pos == food:
            color = "#fecaca"
            symbol = "🍎"
        else:
            color = "#1f2937"
            symbol = ""

        cells.append(
            f'<div class="cell" style="background-color:{color};'
            f'font-size:clamp(8px,2vw,15px);">{symbol}</div>'
        )

board_html = (
    '<div class="board">'
    + "".join(cells)
    + '</div>'
)

st.markdown(board_html, unsafe_allow_html=True)

# Show game-over message or controls
if st.session_state.over:
    st.error(f"Game Over! Final score: {st.session_state.score}")

    if st.button("🔄 Play Again", use_container_width=True):
        new_game()
        st.rerun()

else:
    st.markdown(
        "<h3>Controls</h3>",
        unsafe_allow_html=True
    )

    # Up button
    _, middle, _ = st.columns(3, gap="small")

    with middle:
        if st.button("⬆️", key="up", use_container_width=True):
            turn((0, -1))

    # Left, down, and right buttons
    left, middle, right = st.columns(3, gap="small")

    with left:
        if st.button("⬅️", key="left", use_container_width=True):
            turn((-1, 0))

    with middle:
        if st.button("⬇️", key="down", use_container_width=True):
            turn((0, 1))

    with right:
        if st.button("➡️", key="right", use_container_width=True):
            turn((1, 0))

    if st.button("🔄 Restart", use_container_width=True):
        new_game()
        st.rerun()
