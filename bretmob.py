import streamlit as st
import random
import time

# Constants
GRID_SIZE = 10
BOX_PAYOFF = 10
GAME_DURATION = 180  # seconds

# Session state initialization
if 'bomb_location' not in st.session_state:
    st.session_state.bomb_location = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
if 'clicked_boxes' not in st.session_state:
    st.session_state.clicked_boxes = set()
if 'total_payoff' not in st.session_state:
    st.session_state.total_payoff = 0
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'game_stopped' not in st.session_state:
    st.session_state.game_stopped = False
if 'bomb_clicked' not in st.session_state:
    st.session_state.bomb_clicked = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# Helper functions
def restart_game():
    st.session_state.bomb_location = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    st.session_state.clicked_boxes = set()
    st.session_state.total_payoff = 0
    st.session_state.game_started = False
    st.session_state.game_stopped = False
    st.session_state.bomb_clicked = False
    st.session_state.start_time = None

def get_remaining_time():
    if st.session_state.start_time is None:
        return GAME_DURATION
    elapsed = time.time() - st.session_state.start_time
    return max(0, int(GAME_DURATION - elapsed))

# UI
st.markdown("<h1 style='text-align: center; color: red;'>BRET</h1>", unsafe_allow_html=True)

# Info and controls
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.markdown("**1 box = 10 points**")
    st.markdown("**Bomb = 0 points**")
with col2:
    st.markdown(f"**Boxes Clicked:** {len(st.session_state.clicked_boxes)}")
    st.markdown(f"**Total Payoff:** {st.session_state.total_payoff} points")
with col3:
    remaining_time = get_remaining_time()
    st.markdown(f"⏱ **Time Left:** {remaining_time // 60}:{remaining_time % 60:02}")

# Start / Stop buttons
col1, col2 = st.columns(2)
with col1:
    if not st.session_state.game_started:
        if st.button("▶️ Start Game"):
            st.session_state.game_started = True
            st.session_state.start_time = time.time()
with col2:
    if st.session_state.game_started and not st.session_state.game_stopped:
        if st.button("⏹️ Stop Game"):
            st.session_state.game_stopped = True
            st.rerun()

# Timer enforcement
if st.session_state.game_started and not st.session_state.game_stopped and get_remaining_time() == 0:
    st.session_state.game_stopped = True
    st.rerun()

# Grid UI with clickable boxes
if st.session_state.game_started:
    for i in range(GRID_SIZE):
        cols = st.columns(GRID_SIZE)
        for j in range(GRID_SIZE):
            cell_key = f"box_{i}_{j}"
            clicked = (i, j) in st.session_state.clicked_boxes
            is_bomb = (i, j) == st.session_state.bomb_location

            color = "#e6f2ff"
            label = ""
            border = "1px solid #99c2ff"

            if st.session_state.game_stopped:
                if is_bomb:
                    color = "#ff6666"
                    label = "💣"
                elif clicked:
                    color = "#66cc66"
                    label = "$"
            elif clicked:
                color = "#b3d9ff"
                label = "✔️"

            box_html = f"<div style='padding:8px;background-color:{color};text-align:center;color:white;border-radius:6px;font-size:16px;border:{border}'>{label or '&nbsp;'}</div>"

            if not clicked and not st.session_state.game_stopped:
                if cols[j].button(" ", key=cell_key):
                    if (i, j) == st.session_state.bomb_location:
                        st.session_state.bomb_clicked = True
                    st.session_state.clicked_boxes.add((i, j))
                    if not st.session_state.bomb_clicked:
                        st.session_state.total_payoff += BOX_PAYOFF
                    st.rerun()
            else:
                cols[j].markdown(box_html, unsafe_allow_html=True)

# Bomb reveal after stop
if st.session_state.game_stopped:
    st.markdown(f"**Bomb was at:** {st.session_state.bomb_location}")

# Restart
if st.button("🔁 Restart Game"):
    restart_game()
    st.rerun()
