# BRET Game - Mobile Compatible Version

import streamlit as st
import random
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="BRET", layout="wide")

# --- Initialize session states ---
if 'grid' not in st.session_state:
    st.session_state.grid = [None] * 100
    st.session_state.bombs = random.sample(range(100), 5)
    st.session_state.clicked = set()
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.total_payoff = 0
    st.session_state.bomb_clicked_at = None

# --- Timer logic ---
TIME_LIMIT = 180  # 3 minutes
elapsed_time = int(time.time() - st.session_state.start_time)
remaining_time = max(0, TIME_LIMIT - elapsed_time)

if remaining_time == 0 and not st.session_state.game_over:
    st.session_state.game_over = True
    if st.session_state.bomb_clicked_at:
        st.session_state.total_payoff = 0

# --- Title ---
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>BRET</h1>", unsafe_allow_html=True)

# --- Timer Display ---
st.markdown(f"<h4 style='text-align: center;'>⏳ Time remaining: {remaining_time} seconds</h4>", unsafe_allow_html=True)

# --- Function to handle box click ---
def click_box(i):
    if st.session_state.game_over:
        return
    if i in st.session_state.clicked:
        return
    st.session_state.clicked.add(i)
    if i in st.session_state.bombs:
        st.session_state.bomb_clicked_at = i
        st.session_state.total_payoff = 0  # Will show at end
    else:
        st.session_state.total_payoff += 1

# --- Grid UI ---
st.markdown("""
<style>
.grid-container {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 10px;
  justify-items: center;
}
.box {
  width: 100%;
  max-width: 50px;
  aspect-ratio: 1 / 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #3498db;
  color: white;
  font-weight: bold;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  font-size: 18px;
  border: none;
}
.clicked {
  background-color: #2ecc71 !important;
}
</style>
""", unsafe_allow_html=True)

box_html = "<div class='grid-container'>"
for i in range(100):
    if i in st.session_state.clicked:
        color = 'clicked'
        label = ''
    else:
        color = ''
        label = ''
    box_html += f"<button class='box {color}' onclick=\"window.location.search='?click={i}'\">{label or '&nbsp;'}</button>"
box_html += "</div>"
st.markdown(box_html, unsafe_allow_html=True)

# --- Handle box click from query params ---
params = st.query_params
click = params.get("click", [None])[0]

if click is not None and click.isdigit():
    index = int(click)
    click_box(index)
    st.query_params.clear()
    st.experimental_rerun()

# --- Show results after game ends ---
if st.session_state.game_over:
    st.markdown("---")
    st.markdown("<h3 style='color: #e74c3c;'>Game Over</h3>", unsafe_allow_html=True)
    if st.session_state.bomb_clicked_at is not None:
        st.markdown(f"**Bomb was at:** {st.session_state.bomb_clicked_at}")
        st.markdown(f"**💣 You hit a bomb! Total payoff: 0**")
    else:
        st.markdown(f"**✅ Total boxes clicked: {len(st.session_state.clicked)}**")
        st.markdown(f"**💰 Total payoff: {st.session_state.total_payoff}**")
else:
    if len(st.session_state.clicked) == 100:
        st.session_state.game_over = True
        st.experimental_rerun()

# --- Footer Aesthetic ---
st.markdown("<hr style='margin-top: 50px;'>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: grey;'>A behavioral game inspired by BRET</div>", unsafe_allow_html=True)
