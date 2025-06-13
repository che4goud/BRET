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
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'withdrawn' not in st.session_state:
    st.session_state.withdrawn = False
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
    st.session_state.game_over = False
    st.session_state.withdrawn = False
    st.session_state.bomb_clicked = False
    st.session_state.start_time = time.time()

# Game logic
def select_box(key):
    if st.session_state.withdrawn:
        return

    row, col = map(int, key.split('_'))
    if (row, col) not in st.session_state.selected_boxes:
        st.session_state.selected_boxes.add((row, col))
        if (row, col) == st.session_state.bomb_location:
            st.session_state.bomb_clicked = True
        else:
            st.session_state.total_payoff += BOX_PAYOFF

# Interface
st.title("Bomb Risk Elicitation Task (BRET) - Concealed Version")
st.markdown("**Instructions**: Click boxes to select them. You won't see the rewards until you withdraw. Avoid the bomb! If you click it, your payout becomes ₹0. Withdraw anytime to see your result.")

# Show timer
remaining_time = get_remaining_time()
st.markdown(f"### ⏳ Time Left: {remaining_time // 60:02d}:{remaining_time % 60:02d}")

# Display grid
grid = st.empty()
with grid.container():
    for i in range(GRID_SIZE):
        cols = st.columns(GRID_SIZE)
        for j in range(GRID_SIZE):
            label = "❓"
            box_color = "gray"

            if (i, j) in st.session_state.selected_boxes:
                if st.session_state.withdrawn:
                    if (i, j) == st.session_state.bomb_location:
                        label = "💣"
                        box_color = "red"
                    else:
                        label = "💎"
                        box_color = "green"
                else:
                    label = "✔️"
                    box_color = "blue"

            key = f"{i}_{j}"
            if not st.session_state.withdrawn and remaining_time > 0:
                if cols[j].button(label, key=key):
                    select_box(key)
            else:
                cols[j].markdown(f"<div style='padding:8px;background-color:{box_color};text-align:center;color:white;border-radius:4px;font-size:20px'>{label}</div>", unsafe_allow_html=True)

# Controls
st.write("---")
if not st.session_state.withdrawn:
    if st.button("Withdraw and Reveal Payout"):
        if st.session_state.bomb_clicked:
            st.session_state.total_payoff = 0
        st.session_state.withdrawn = True
        st.rerun()
else:
    st.success(f"You withdrew with a total payout of ₹{st.session_state.total_payoff}.")

if st.button("Restart Game"):
    restart_game()
    st.rerun()
