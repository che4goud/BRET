# BRET Game - Mobile Compatible Version

import streamlit as st
import random
import time

st.set_page_config(page_title="BRET", layout="wide")

# --- Constants ---
GRID_SIZE = 10
NUM_BOMBS = 5
TIME_LIMIT = 180  # seconds

# --- Session State Initialization ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.start_time = None
    st.session_state.bombs = []
    st.session_state.clicked = set()
    st.session_state.total_payoff = 0
    st.session_state.bomb_clicked_at = None
    st.session_state.game_over = False

def start_game():
    st.session_state.game_started = True
    st.session_state.start_time = time.time()
    st.session_state.bombs = random.sample(range(GRID_SIZE * GRID_SIZE), NUM_BOMBS)
    st.session_state.clicked = set()
    st.session_state.total_payoff = 0
    st.session_state.bomb_clicked_at = None
    st.session_state.game_over = False

def restart_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def end_game():
    st.session_state.game_over = True

# --- Timer Logic ---
if st.session_state.game_started and not st.session_state.game_over:
    elapsed_time = int(time.time() - st.session_state.start_time)
    remaining_time = max(0, TIME_LIMIT - elapsed_time)
    if remaining_time == 0:
        st.session_state.game_over = True
        st.session_state.total_payoff = 0
else:
    remaining_time = TIME_LIMIT

# --- Header ---
st.markdown("<h1 style='text-align:center; color:#ff4b4b;'>BRET</h1>", unsafe_allow_html=True)

# --- Controls ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶️ Start Game"):
        start_game()
        st.rerun()
with col2:
    if st.button("🔁 Restart Game"):
        restart_game()
with col3:
    if st.button("⛔ End Game"):
        end_game()

st.markdown(f"<h4 style='text-align:center;'>⏳ Time Remaining: {remaining_time} seconds</h4>", unsafe_allow_html=True)

# --- Gameplay Grid ---
def click_box(i):
    if st.session_state.game_over or i in st.session_state.clicked:
        return
    st.session_state.clicked.add(i)
    if i in st.session_state.bombs:
        st.session_state.bomb_clicked_at = i
        st.session_state.total_payoff = 0
        st.session_state.game_over = True
    else:
        st.session_state.total_payoff += 1

if st.session_state.game_started:
    for row in range(GRID_SIZE):
        cols = st.columns(GRID_SIZE)
        for col in range(GRID_SIZE):
            i = row * GRID_SIZE + col
            label = " "
            disabled = i in st.session_state.clicked or st.session_state.game_over
            if i in st.session_state.clicked:
                if i == st.session_state.bomb_clicked_at:
                    label = "💣"
                else:
                    label = "✅"
            cols[col].button(label, key=f"box_{i}", on_click=click_box, args=(i,), disabled=disabled)

# --- End Game Results ---
if st.session_state.game_over:
    st.markdown("---")
    st.markdown("<h3 style='color:#e74c3c;'>Game Over</h3>", unsafe_allow_html=True)
    if st.session_state.bomb_clicked_at is not None:
        st.markdown(f"**Bomb was at:** {st.session_state.bomb_clicked_at} 💣")
        st.markdown("**💥 You hit a bomb! Payoff: 0**")
    else:
        st.markdown(f"**✅ Safe boxes clicked: {len(st.session_state.clicked)}**")
        st.markdown(f"**💰 Total payoff: {st.session_state.total_payoff}**")

# --- Footer ---
st.markdown("<hr style='margin-top: 50px;'>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: grey;'>A behavioral game inspired by BRET</div>", unsafe_allow_html=True)

