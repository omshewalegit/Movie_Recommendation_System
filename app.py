import streamlit as st
import pickle
import pandas as pd
import requests
from urllib.parse import quote
import time
import os

# Configure Streamlit page
st.set_page_config(
    page_title="CineSuggest",
    page_icon="🎬",
    layout="wide"
)

# Load data with error handling
@st.cache_data
def load_data():
    try:
        movies = pickle.load(open('movies.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        return movies, similarity
    except Exception as e:
        st.error(f"Error loading data files: {str(e)}")
        return None, None

movies, similarity = load_data()

if movies is None or similarity is None:
    st.stop()

st.title('🎬 CineSuggest')
st.markdown("Discover movies you'll love more based on your favorites")

def fix_movie_title(title):
    """Fix movie title capitalization"""
    if not title:
        return title
    
    lowercase_words = {'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'if', 'in', 
                      'nor', 'of', 'on', 'or', 'so', 'the', 'to', 'up', 'yet', 'with'}
    
    words = title.split()
    fixed_words = []
    
    for i, word in enumerate(words):
        if i == 0 or (i > 0 and words[i-1].endswith(':')):
            fixed_words.append(word.capitalize())
        elif word.lower() in lowercase_words:
            fixed_words.append(word.lower())
        else:
            fixed_words.append(word.capitalize())
    
    return ' '.join(fixed_words)

def get_movie_poster_omdb(movie_title, retries=2):
    """Fetch movie poster from OMDb API with retries"""
    api_key = "10f3c387"  # Updated API key
    
    for attempt in range(retries + 1):
        try:
            clean_title = movie_title.strip()
            encoded_title = quote(clean_title)
            url = f"https://www.omdbapi.com/?apikey={api_key}&t={encoded_title}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == 'True':
                    poster_url = data.get('Poster')
                    imdb_id = data.get('imdbID')
                    year = data.get('Year')
                    director = data.get('Director')
                    genre = data.get('Genre')
                    plot = data.get('Plot')
                    if poster_url and poster_url != 'N/A' and poster_url.startswith('http'):
                        return {
                            'poster': poster_url,
                            'imdb_id': imdb_id,
                            'imdb_url': f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else None,
                            'year': year,
                            'director': director,
                            'genre': genre,
                            'plot': plot,
                            'success': True
                        }
            if attempt == retries:
                return {'success': False, 'error': f"OMDb Error: {data.get('Error', 'Unknown error')}"}
        except Exception as e:
            if attempt == retries:
                return {'success': False, 'error': str(e)}
        time.sleep(1)
    return {'success': False, 'error': "Max retries exceeded"}

def get_fallback_poster(movie_title):
    title_short = movie_title[:25] + "..." if len(movie_title) > 25 else movie_title
    encoded_title = quote(title_short)
    return f"https://via.placeholder.com/300x450/34495e/ecf0f1?text={encoded_title}"

@st.cache_data(ttl=3600)
def get_movie_data(movie_title):
    result = get_movie_poster_omdb(movie_title)
    if result.get('success'):
        return result
    else:
        return {
            'poster': get_fallback_poster(movie_title),
            'imdb_url': f"https://www.imdb.com/find?q={quote(movie_title)}",
            'success': False,
            'error': result.get('error', 'Unknown error')
        }

def recommend(movie):
    try:
        movie_indices = movies[movies['title'] == movie].index
        if len(movie_indices) == 0:
            return [], "Movie not found in database"
        movie_idx = movie_indices[0]
        distances = similarity[movie_idx]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
        recommended_movies = [movies.iloc[i[0]].title for i in movies_list]
        return recommended_movies, None
    except Exception as e:
        return [], f"Error generating recommendations: {str(e)}"

# Set default number of recommendations
max_recommendations = 10

# Main interface
col1, col2 = st.columns([3, 1])

with col1:
    movies_list = movies['title'].values
    selected_movie = st.selectbox("Choose a movie to get recommendations:", movies_list, index=0)

with col2:
    st.write("")
    st.write("")
    recommend_button = st.button('🎬 Get Recommendations', type="primary")

if recommend_button and selected_movie:
    with st.spinner('🔍 Finding similar movies...'):
        recommendations, error = recommend(selected_movie)
    
    if error:
        st.error(f"Error: {error}")
    elif recommendations:
        recommendations = recommendations[:max_recommendations]
        tab1, tab2 = st.tabs(["🖼 Poster View", "📝 Details View"])
        
        with tab1:
            cols = st.columns(3)
            for idx, movie in enumerate(recommendations):
                with cols[idx % 3]:
                    movie_data = get_movie_data(movie)
                    try:
                        st.image(movie_data['poster'], width=200, caption=fix_movie_title(movie))
                    except:
                        st.markdown("🎭 No Poster")
        
        with tab2:
            for idx, movie in enumerate(recommendations, 1):
                movie_data = get_movie_data(movie)
                col1, col2 = st.columns([1, 3])
                with col1:
                    try:
                        st.image(movie_data['poster'], width=250)  # Increased poster size
                    except:
                        st.markdown("🎭 No Poster")
                with col2:
                    st.markdown(f"### {idx}. {fix_movie_title(movie)}")
                    if movie_data.get('year'):
                        st.write(f"*Year:* {movie_data['year']}")
                    if movie_data.get('director') and movie_data['director'] != 'N/A':
                        st.write(f"*Director:* {movie_data['director']}")
                    if movie_data.get('genre') and movie_data['genre'] != 'N/A':
                        st.write(f"*Genre:* {movie_data['genre']}")
                    if movie_data.get('plot') and movie_data['plot'] != 'N/A':
                        st.write(f"*Plot:* {movie_data['plot'][:200]}...")
                    if movie_data.get('imdb_url'):
                        st.markdown(f"[🎬 View on IMDb]({movie_data['imdb_url']})")
                st.divider()
    else:
        st.warning("No recommendations found. Please try a different movie.")