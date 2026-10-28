
import streamlit as st
import random
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Snake Game",
    page_icon="🐍",
    layout="centered"
)

st.title("🐍 Snake Game")
st.caption("Eat the apples, grow your snake, and beat your high score!")

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

# Change direction, but don't allow a reverse turn
def turn(new_direction):
    dx, dy = st.session_state.direction
    nx, ny = new_direction

    if (nx, ny) != (-dx, -dy):
        st.session_state.direction = new_direction

# Direction buttons
st.write("### Controls")

row1 = st.columns([1, 1, 1])
with row1[1]:
    if st.button("⬆️ Up", use_container_width=True):
        turn((0, -1))

row2 = st.columns(3)
with row2[0]:
    if st.button("⬅️ Left", use_container_width=True):
        turn((-1, 0))
with row2[1]:
    if st.button("⬇️ Down", use_container_width=True):
        turn((0, 1))
with row2[2]:
    if st.button("➡️ Right", use_container_width=True):
        turn((1, 0))

# Move the snake on each automatic refresh
if not st.session_state.over:
    st_autorefresh(interval=300, key="snake_timer")

    dx, dy = st.session_state.direction
    x, y = st.session_state.snake[0]
    head = (x + dx, y + dy)

    eating = head == st.session_state.food
    body = (
        st.session_state.snake
        if eating
        else st.session_state.snake[:-1]
    )

    # Check wall and body collisions
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

# Display score
st.metric("🏆 Score", st.session_state.score)

# Draw the board
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
            f'<div style="background:{color};aspect-ratio:1;'
            f'display:flex;align-items:center;justify-content:center;'
            f'font-size:clamp(9px,2.5vw,18px);border-radius:3px;">'
            f'{symbol}</div>'
        )

board = (
    '<div style="display:grid;'
    'grid-template-columns:repeat(15,minmax(0,1fr));'
    'gap:2px;width:100%;max-width:450px;margin:12px auto;">'
    + "".join(cells)
    + "</div>"
)

st.markdown(board, unsafe_allow_html=True)

if st.session_state.over:
    st.error("Game Over! Final score: " + str(st.session_state.score))

    if st.button("🔄 Play Again", use_container_width=True):
        new_game()
        st.rerun()

st.caption("Tip: Use the buttons above the board to steer your snake.")
