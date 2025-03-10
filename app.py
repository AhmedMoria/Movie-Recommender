import streamlit as st
import requests
import joblib
from datetime import datetime

st.set_page_config(
    page_title="ShadowFlix",
    page_icon="🎥",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #0A0F1E, #102A43);
            color: #D1E8E2;
            font-family: 'Poppins', sans-serif;
        }
        .main-title {
            font-size: 3em;
            font-weight: bold;
            color: #A8DADC;
            text-align: center;
            margin-bottom: 10px;
            text-shadow: 3px 3px 6px rgba(168, 218, 220, 0.6);
        }
        .card {
            background: #1B263B;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.5);
        }
        .stButton>button {
            background-color: #457B9D;
            color: #FFFFFF;
            font-size: 1.2em;
            padding: 14px 28px;
            border-radius: 12px;
            font-weight: bold;
            border: none;
            transition: background 0.3s;
        }
        .stButton>button:hover {
            background-color: #1D3557;
        }
        .recommend-box {
            background: #1D3557;
            color: #A8DADC;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            margin: 10px;
            box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.5);
        }
        .recommend-box img {
            border-radius: 8px;
            height: 220px;
            width: 100%;
            object-fit: cover;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""<div class="main-title">🎥 ShadowFlix</div>""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏠 Home", "📋 Recommender", "💬 Feedback"])

with tab1:
    st.markdown("""
        <div class="card">
            <h3 style="color:#A8DADC">👤 About Ahmed</h3>
            <p>
                Hi! I'm Ahmed, a data scientist specializing in machine learning, deep learning, and NLP.
                My passion lies in building intelligent systems and web applications that enhance user experiences.
            </p>
        </div>
        <div class="card">
            <h3 style="color:#A8DADC">🚀 Project Overview</h3>
            <p>
                This AI-driven movie recommendation system provides personalized suggestions
                using advanced machine learning and NLP techniques.
            </p>
        </div>
    """, unsafe_allow_html=True)

with tab2:
    def fetch_poster(movie_id):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path', '')
        return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""

    def recommend(movie):
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters

    movies = joblib.load(open('movie_list.pkl', 'rb'))
    similarity = joblib.load(open('similarity_compressed.pkl', 'rb'))
    selected_movie = st.selectbox("Choose a Movie 🎥", movies['title'].values)

    if st.button('🔮 Get Recommendations'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        for name, poster in zip(recommended_movie_names, recommended_movie_posters):
            st.markdown(f"""
                <div class="recommend-box">
                    <img src="{poster}" alt="{name}">
                    <p><b>{name}</b></p>
                </div>
            """, unsafe_allow_html=True)

with tab3:
    name = st.text_input("Name")
    feedback = st.text_area("Your Feedback")

    if st.button("🚀 Submit Feedback"):
        if name and feedback:
            with open("feedback.txt", "a") as f:
                f.write(f"{datetime.now().date()} - {name}: {feedback}\n")
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please enter both name and feedback.")

    try:
        with open("feedback.txt", "r") as f:
            for line in f.readlines():
                st.markdown(f"<div class='recommend-box'>{line}</div>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.info("No feedback has been received yet.")
