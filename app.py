import streamlit as st
from mood_analyzer import analyze_mood
from spotify_utils import get_spotify_recommendations

st.set_page_config(page_title="Text2Tunes", page_icon="🎧", layout="centered")

st.markdown("""
    <style>
    body {
        margin: 0;
        padding: 0;
        width: 100%;
    }
    .block-container {
        padding-left: 0;
        padding-right: 0;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <h1 style='text-align: center; color: #1DB954;'>🎶 Text2Tunes - Mood Based Music Recommendation 🎶</h1>
    <p style='text-align: center;'>Discover songs that match your vibe!</p>
    <hr style="border-top: 1px solid #bbb;">
    """,
    unsafe_allow_html=True
)

with st.container():
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    st.subheader("🧠 How are you feeling today?")
    
    st.markdown("""
    <style>
    .big-text-input input {
        font-size: 24px;
        padding: 10px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    mood = st.text_input("Enter your current mood...", key="mood", help="Please enter a mood like happy, sad, relaxed, etc.", placeholder="e.g. happy, excited...")

    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

num_songs = st.slider("How many songs would you like to listen?", min_value=1, max_value=20, value=10, step=1)

if mood:
    st.success(f"✅ Detected mood: **{mood}**")

    best_genre = analyze_mood(mood)
    st.info(f"🎧 Based on your mood, you might enjoy the following genres:")

    st.markdown(f"""
    <div style="display: flex; flex-wrap: wrap; justify-content: center;">
        {''.join([f'<div style="background-color: #1DB954; color: white; padding: 8px 20px; border-radius: 20px; margin: 5px;">{genre}</div>' for genre in best_genre])}
    </div>
    """, unsafe_allow_html=True)

    recommendations = get_spotify_recommendations(best_genre, num_songs=num_songs)

    st.markdown("---")
    st.subheader(f"🎵 Recommended Songs for You (Top {num_songs}):")

    card_container = ""
    for idx, track in enumerate(recommendations, start=1):
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        spotify_url = track['external_urls']['spotify']
        album_image_url = track['album']['images'][0]['url']

        card_container += f"""
        <div style="display: flex; align-items: center; padding: 10px; border-radius: 15px; border: 1px solid #ddd; box-shadow: 2px 2px 10px #ccc; margin-bottom: 20px;">
            <img src="{album_image_url}" width="100" height="100" style="border-radius: 10px; margin-right: 20px;">
            <div>
                <h4 style="margin: 0;">{idx}. {track_name}</h4>
                <p style="margin: 5px 0;">by <strong>{artist_name}</strong></p>
                <a href="{spotify_url}" target="_blank" style="color: #1DB954; text-decoration: none; font-weight: bold;">▶️ Listen on Spotify</a>
            </div>
        </div>
        """

    st.markdown(card_container, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Made with ❤️ using Streamlit by Ankit")
