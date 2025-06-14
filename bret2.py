import streamlit as st
import random
import numpy as np
import time

# Configurations
GRID_SIZE = 10
BOX_PAYOFF = 10
TIMER_DURATION = 3 * 60  # 3 minutes in seconds

# Initialize session state
if 'bomb_location' not in st.session_state:
    st.session_state.bomb_location = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
if 'selected_boxes' not in st.session_state:
    st.session_state.selected_boxes = set()
if 'total_payoff' not in st.session_state:
    st.session_state.total_payoff = 0
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'game_stopped' not in st.session_state:
    st.session_state.game_stopped = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'bomb_clicked' not in st.session_state:
    st.session_state.bomb_clicked = False

# Timer logic
def get_remaining_time():
    elapsed = time.time() - st.session_state.start_time
    return max(0, TIMER_DURATION - int(elapsed))

def restart_game():
    st.session_state.bomb_location = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    st.session_state.selected_boxes = set()
    st.session_state.total_payoff = 0
    st.session_state.game_started = False
    st.session_state.game_stopped = False
    st.session_state.bomb_clicked = False
    st.session_state.start_time = time.time()

# Game logic
def select_box(key):
    if not st.session_state.game_started or st.session_state.game_stopped:
        return

    row, col = map(int, key.split('_'))
    if (row, col) not in st.session_state.selected_boxes:
        st.session_state.selected_boxes.add((row, col))
        if (row, col) == st.session_state.bomb_location:
            st.session_state.bomb_clicked = True
        else:
            st.session_state.total_payoff += BOX_PAYOFF

# Interface
st.title("Bomb Risk Elicitation Task (BRET) - Enhanced Version")

# Controls: Start and Stop
if not st.session_state.game_started:
    if st.button("Start"):
        st.session_state.game_started = True
        st.session_state.start_time = time.time()
else:
    remaining_time = get_remaining_time()
    st.markdown(f"### ⏳ Time Left: {remaining_time // 60:02d}:{remaining_time % 60:02d}")

    if st.button("Stop"):
        st.session_state.game_stopped = True
        if st.session_state.bomb_clicked:
            st.session_state.total_payoff = 0
        st.rerun()

# Display grid
grid = st.empty()
with grid.container():
    for i in range(GRID_SIZE):
        cols = st.columns(GRID_SIZE)
        for j in range(GRID_SIZE):
            label = ""
            box_color = "lightgray"
            border_style = "2px solid transparent"

            key = f"{i}_{j}"
            clicked = (i, j) in st.session_state.selected_boxes

            if clicked:
                box_color = "#d0e6ff"  # light blue background
                border_style = "3px solid #004080"  # dark blue border
                label = "✔️"

            if st.session_state.game_stopped:
                if (i, j) == st.session_state.bomb_location:
                    label = "💣"
                    box_color = "red"
                    border_style = "3px solid darkred"
                elif clicked:
                    label = "$"
                    box_color = "green"
                    border_style = "3px solid darkgreen"

            if st.session_state.game_started and not st.session_state.game_stopped:
                if clicked:
                    # Show non-interactive clicked box
                    cols[j].markdown(
                        f"<div style='padding:8px;background-color:{box_color};text-align:center;color:white;border-radius:4px;font-size:20px;border:{border_style}'>{label}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    if cols[j].button("", key=key, help=f"Box {i},{j}"):
                        select_box(key)
            else:
                cols[j].markdown(
                    f"<div style='padding:8px;background-color:{box_color};text-align:center;color:white;border-radius:4px;font-size:20px;border:{border_style}'>{label}</div>",
                    unsafe_allow_html=True
                )

# Display summary
st.write("---")
st.markdown(f"### 📦 Boxes Clicked: {len(st.session_state.selected_boxes)}")
if st.session_state.game_stopped:
    st.markdown(f"### 💰 Total Points Earned: {st.session_state.total_payoff}")

# Restart
if st.button("Restart Game"):
    restart_game()
    st.rerun()
