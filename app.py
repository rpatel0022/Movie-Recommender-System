
import pickle
import streamlit as st
import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for styling
st.markdown(
    """
<style>
    .main {
        padding-top: 2rem;
    }

    .title-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .title-text {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        letter-spacing: -0.5px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .subtitle-text {
        color: #f0f0f0;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        font-weight: 400;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .movie-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-align: center;
        margin: 0.5rem;
        border: 1px solid #e0e0e0;
        height: 100%;
    }

    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }

    .movie-title {
        font-weight: 600;
        font-size: 0.95rem;
        color: #2c3e50;
        margin: 0.75rem 0 0 0;
        padding: 0 0.25rem;
        line-height: 1.3;
        min-height: 2.6rem;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .recommendation-container {
        padding: 2rem 0;
    }

    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #667eea;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        letter-spacing: 0.3px;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    .loading-container {
        text-align: center;
        padding: 2rem;
    }

    .recommendations-header {
        text-align: center;
        color: #2c3e50;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 2rem 0 1.5rem 0;
        position: relative;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        letter-spacing: -0.3px;
    }

    .recommendations-header::after {
        content: '';
        display: block;
        width: 80px;
        height: 3px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: 0.75rem auto;
        border-radius: 2px;
    }

    .selection-container {
        background: #f8f9fa;
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }

    .selection-label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        text-align: center;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
</style>
""",
    unsafe_allow_html=True,
)


def fetch_poster(movie_id):
    try:
        # Get API key from environment variables
        api_key = os.getenv("TMDB_API_KEY")
        if not api_key:
            st.error(
                "🚨 TMDB API key not found. Please check your environment variables."
            )
            return "https://via.placeholder.com/500x750/cccccc/666666?text=No+API+Key"

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        data = requests.get(url)
        data = data.json()
        poster_path = data["poster_path"]
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except Exception as e:
        st.warning(f"Could not fetch poster for movie ID {movie_id}")
        return "https://via.placeholder.com/500x750/cccccc/666666?text=No+Image"


def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1]
    )
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# Header Section
st.markdown(
    """
<div class="title-container">
    <h1 class="title-text">🎬 Movie Recommender</h1>
    <p class="subtitle-text">Tell us a movie you loved, and we'll find similar movies perfect for you</p>
</div>
""",
    unsafe_allow_html=True,
)


# Load data
@st.cache_data
def load_data():
    similarity = pickle.load(open("similarity.pkl", "rb"))
    movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
    movies = pd.DataFrame(movies_dict)
    return similarity, movies


try:
    similarity, movies = load_data()
    movie_list = movies["title"].values

    # Movie selection section
    st.markdown(
        """
        <div class="selection-container">
            <p class="selection-label">🎯 Select a movie you really enjoyed watching:</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_movie = st.selectbox(
        "",
        movie_list,
        help="Search for a movie you enjoyed - we'll find similar ones you'll love!",
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        recommend_button = st.button(
            "🎬 Find Movies Like This", use_container_width=True
        )

    # Recommendations section
    if recommend_button:
        with st.spinner("🎭 Finding perfect matches for you..."):
            time.sleep(1)  # Small delay for better UX
            recommended_movie_names, recommended_movie_posters = recommend(
                selected_movie
            )

        st.markdown(
            '<h2 class="recommendations-header">🎯 Movies Similar to Your Choice</h2>',
            unsafe_allow_html=True,
        )

        # Display recommendations in a more attractive layout
        cols = st.columns(5, gap="medium")

        for idx, (col, name, poster) in enumerate(
                zip(cols, recommended_movie_names, recommended_movie_posters)
        ):
            with col:
                st.markdown(
                    f"""
                    <div class="movie-card">
                        <img src="{poster}" style="width: 100%; border-radius: 10px; margin-bottom: 0.5rem;">
                        <div class="movie-title">{name}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Add some spacing and encouragement
        st.markdown("---")
        st.markdown(
            '<div style="text-align: center; margin: 2rem 0;">'
            "<h3 style=\"color: #2c3e50; font-size: 1.3rem; font-weight: 600; margin-bottom: 0.5rem; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;\">🎬 Perfect matches for your taste! 🍿</h3>"
            "<p style=\"color: #666; font-size: 1rem; font-style: italic; margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;\">Love one of these recommendations? Use it to discover even more great movies!</p>"
            "</div>",
            unsafe_allow_html=True,
        )

except FileNotFoundError as e:
    st.error(
        "🚨 Required files not found. Please ensure 'similarity.pkl' and 'movies_dict.pkl' are in the same directory."
    )
    st.info(
        "💡 Make sure you have the following files in your project folder:\n- similarity.pkl\n- movies_dict.pkl"
    )
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please check your data files and try again.")
