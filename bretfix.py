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

# Timer setup
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# Timer logic
def get_remaining_time():
    if st.session_state.start_time is None:
        return 180
    import time
    elapsed = time.time() - st.session_state.start_time
    return max(0, 180 - int(elapsed))

# Title
st.markdown("<h1 style='text-align: center; color: #2e7bcf;'>💣 BRET - Bomb Risk Elicitation Task 💣</h1>", unsafe_allow_html=True)

# Audio for bomb
bomb_sound_html = """
<audio id='bomb-sound' src='https://www.soundjay.com/button/sounds/beep-07.mp3' preload='auto'></audio>
<script>
function playBombSound() {
  var snd = document.getElementById("bomb-sound");
  snd.play();
}
</script>
"""
st.markdown(bomb_sound_html, unsafe_allow_html=True)

with st.container():
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown("**1 box = 10 points**")
        st.markdown("**Bomb = 0 points**")
    with col2:
        st.markdown(f"**Boxes Clicked:** {min(st.session_state.selected_index, GRID_SIZE * GRID_SIZE)}")
        if st.session_state.game_stopped and st.session_state.bomb_clicked_at != get_row_col(st.session_state.selected_index - 1):
            st.markdown("**Bomb was at:** revealed after game ends")
            if st.session_state.bomb_clicked_at:
                st.session_state.total_payoff = 0
        
    with col3:
        if st.session_state.game_started and not st.session_state.game_stopped:
            st.markdown(f"**Time Left:** {get_remaining_time() // 60:02d}:{get_remaining_time() % 60:02d}")

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

# Timer enforcement
if st.session_state.start_time and get_remaining_time() == 0:
    st.session_state.game_stopped = True
    st.rerun()

# Gameplay
if st.session_state.game_started and not st.session_state.game_stopped:
    if st.button("Click Next Box"):
        if st.session_state.start_time is None:
            import time
            st.session_state.start_time = time.time()
        row, col = get_row_col(st.session_state.selected_index)
        if (row, col) == st.session_state.bomb_location:
            st.session_state.bomb_clicked_at = (row, col)
            # Trigger bomb audio in UI
            st.components.v1.html("<script>playBombSound();</script>", height=0)
            # Do not stop game immediately; wait for user to press Stop
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

            box_html = f"<div style='padding:10px;background-color:{color};text-align:center;color:white;border-radius:8px;font-size:22px;font-weight:bold;border:{border};box-shadow: 2px 2px 8px rgba(0,0,0,0.2)'>{label or '&nbsp;'}</div>"
            cols[j].markdown(box_html, unsafe_allow_html=True)

# Restart button
if st.button("🔁 Restart Game"):
    restart_game()
    st.rerun()


