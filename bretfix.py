import streamlit as st
import random

GRID_SIZE = 10
BOX_PAYOFF = 10

# Initialize session state
if 'bomb_location' not in st.session_state:
    st.session_state.bomb_location = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
if 'selected_index' not in st.session_state:
    st.session_state.selected_index = 0
if 'total_payoff' not in st.session_state:
    st.session_state.total_payoff = 0
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'game_stopped' not in st.session_state:
    st.session_state.game_stopped = False
if 'bomb_clicked_at' not in st.session_state:
    st.session_state.bomb_clicked_at = None

# Helper functions
def get_row_col(index):
    return index // GRID_SIZE, index % GRID_SIZE

def restart_game():
    st.session_state.bomb_location = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    st.session_state.selected_index = 0
    st.session_state.total_payoff = 0
    st.session_state.game_started = False
    st.session_state.game_stopped = False
    st.session_state.bomb_clicked_at = None

# Interface
st.title("BRET - Sequential No Timer Version")

# Header
with st.container():
    col1, col2 = st.columns([2, 2])
    with col1:
        st.markdown("**1 box = 10 points**")
        st.markdown("**Bomb = 0 points**")
    with col2:
        st.markdown(f"**Boxes Clicked:** {st.session_state.selected_index}")
        if st.session_state.game_stopped and st.session_state.bomb_clicked_at != get_row_col(st.session_state.selected_index - 1):
            st.markdown(f"**Bomb was at:** {st.session_state.bomb_clicked_at}")
            st.markdown(f"**Total Payoff:** {st.session_state.total_payoff} points")

# Start / Stop buttons
col1, col2 = st.columns([1, 1])
with col1:
    if not st.session_state.game_started:
        if st.button("▶️ Start Game"):
            st.session_state.game_started = True

with col2:
    if st.session_state.game_started and not st.session_state.game_stopped:
        if st.button("⏹️ Stop Game"):
            st.session_state.game_stopped = True
            st.rerun()

# Gameplay
if st.session_state.game_started and not st.session_state.game_stopped:
    if st.button("Click Next Box"):
        row, col = get_row_col(st.session_state.selected_index)
        if (row, col) == st.session_state.bomb_location:
            st.session_state.total_payoff = 0
            st.session_state.bomb_clicked_at = (row, col)
            st.session_state.game_stopped = True
        else:
            st.session_state.total_payoff += BOX_PAYOFF
            st.session_state.selected_index += 1
        st.rerun()

# Display grid
with st.container():
    for i in range(GRID_SIZE):
        cols = st.columns(GRID_SIZE)
        for j in range(GRID_SIZE):
            index = i * GRID_SIZE + j
            selected = index < st.session_state.selected_index
            is_bomb = (i, j) == st.session_state.bomb_location

            color = "#e6f2ff"
            label = ""
            border = "2px solid #99c2ff"

            if st.session_state.game_stopped:
                if is_bomb:
                    color = "#ff6666"
                    label = "💣"
                elif selected:
                    color = "#66cc66"
                    label = "$"
            elif selected:
                color = "#b3d9ff"
                label = "✔️"

            box_html = f"<div style='padding:8px;background-color:{color};text-align:center;color:white;border-radius:6px;font-size:20px;border:{border}'>{label or '&nbsp;'}</div>"
            cols[j].markdown(box_html, unsafe_allow_html=True)

# Restart button
if st.button("🔁 Restart Game"):
    restart_game()
    st.rerun()
