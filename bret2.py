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
    st.session_state.start_time = None
if 'bomb_clicked' not in st.session_state:
    st.session_state.bomb_clicked = False
if 'bomb_clicked_at' not in st.session_state:
    st.session_state.bomb_clicked_at = None

# Timer logic
def get_remaining_time():
    if st.session_state.start_time is None:
        return TIMER_DURATION
    elapsed = time.time() - st.session_state.start_time
    return max(0, TIMER_DURATION - int(elapsed))

def restart_game():
    st.session_state.bomb_location = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    st.session_state.selected_boxes = set()
    st.session_state.total_payoff = 0
    st.session_state.game_started = False
    st.session_state.game_stopped = False
    st.session_state.bomb_clicked = False
    st.session_state.bomb_clicked_at = None
    st.session_state.start_time = None

# Game logic
def select_box(key):
    if not st.session_state.game_started or st.session_state.game_stopped:
        return

    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    row, col = map(int, key.split('_'))
    if (row, col) not in st.session_state.selected_boxes:
        st.session_state.selected_boxes.add((row, col))
        if (row, col) == st.session_state.bomb_location:
            st.session_state.bomb_clicked = True
            st.session_state.bomb_clicked_at = (row, col)
        else:
            st.session_state.total_payoff += BOX_PAYOFF

# Check if time expired
if st.session_state.start_time is not None and not st.session_state.game_stopped:
    if get_remaining_time() <= 0:
        st.session_state.game_stopped = True
        if st.session_state.bomb_clicked:
            st.session_state.total_payoff = 0

# Interface
st.title("Bomb Risk Elicitation Task (BRET) - Grid Version")

# Live header
header = st.empty()
def render_header():
    with header.container():
        top1, top2, top3 = st.columns([1.5, 1.5, 3])
        with top1:
            st.markdown("ℹ️ **1 box = 10 points**  ")
            st.markdown("💣 **Bomb = 0 points**  ")
            st.markdown("⏱ **Max time = 3 mins**")
        with top2:
            st.markdown(f"📦 **Boxes Clicked:** {len(st.session_state.selected_boxes)}")
            if st.session_state.bomb_clicked:
                st.markdown(f"💥 **Bomb at:** {st.session_state.bomb_clicked_at}")
        with top3:
            if st.session_state.game_started and not st.session_state.game_stopped:
                remaining_time = get_remaining_time()
                st.markdown(f"⏳ **Time Left:** {remaining_time // 60:02d}:{remaining_time % 60:02d}")
            st.markdown(f"💰 **Total Payoff:** {st.session_state.total_payoff} points")

render_header()

# Controls: Start and Stop
col1, col2 = st.columns([1, 1])
with col1:
    if not st.session_state.game_started:
        if st.button("▶️ Start Game"):
            st.session_state.game_started = True
with col2:
    if st.session_state.game_started and not st.session_state.game_stopped:
        if st.button("⏹️ Stop Game"):
            st.session_state.game_stopped = True
            if st.session_state.bomb_clicked:
                st.session_state.total_payoff = 0
            st.rerun()

# Display grid
st.write("### Click the boxes")
grid = st.container()
with grid:
    for i in range(GRID_SIZE):
        cols = st.columns(GRID_SIZE)
        for j in range(GRID_SIZE):
            key = f"{i}_{j}"
            clicked = (i, j) in st.session_state.selected_boxes

            box_color = "#e6f2ff"
            border_style = "2px solid #99c2ff"
            transition_style = "transition: all 0.3s ease;"
            hover_effect = "box-shadow: 0 0 10px rgba(0, 123, 255, 0.4); cursor: pointer;"
            label = ""

            if clicked:
                box_color = "#b3d9ff"
                border_style = "3px solid #004080"
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

            box_html = f"<div style='padding:8px;background-color:{box_color};text-align:center;color:white;border-radius:6px;font-size:20px;border:{border_style};{transition_style}{hover_effect}'>{label or '&nbsp;'}</div>"

            if clicked or st.session_state.game_stopped or not st.session_state.game_started:
                cols[j].markdown(box_html, unsafe_allow_html=True)
            elif st.session_state.game_started:
                if cols[j].button(" ", key=key):
                    select_box(key)
                    st.rerun()

# Restart
if st.button("🔁 Restart Game"):
    restart_game()
    st.rerun()
