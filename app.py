# # import streamlit as st
# # import pickle
# # import pandas as pd

# # movies = pickle.load(open('movies.pkl','rb'))
# # st.title('Movie Recommender System 🎬')
# # similarity = pickle.load(open('similarity.pkl','rb'))

# # def recommend(movie):
# #     recommend_movies = []
# #     movie_idx = movies[movies['title']==movie].index[0]
# #     distances = similarity[movie_idx]
# #     movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:11]

# #     for i in movies_list:
# #      movie_id = i[0]
# #     #Fetching the poster of the movie form API


# #      recommend_movies.append(movies.iloc[i[0]].title)
# #     return recommend_movies     


# # movies_list = movies['title'].values
# # selected_movie = st.selectbox(
# #     "Choose a movie",
# #      movies_list
# # )

# # if st.button('Recommend'):
# #     recommendations = recommend(selected_movie)
# #     for i in recommendations:
# #      st.write(i)

import streamlit as st
import pickle
import pandas as pd
import requests
from urllib.parse import quote
import concurrent.futures
from threading import Lock

# Load data
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('CineSuggest')

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

def fetch_movie_data_omdb(movie_title):
    """Fetch movie data from OMDb API"""
    try:
        api_key = "81293116"
        clean_title = quote(movie_title.strip())
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={clean_title}&plot=short&r=json"
        
        response = requests.get(url, timeout=2)
        data = response.json()
        
        if response.status_code == 200 and data.get('Response') == 'True':
            poster_url = data.get('Poster')
            imdb_id = data.get('imdbID')
            
            return {
                'poster': poster_url if poster_url != 'N/A' else None,
                'imdb_id': imdb_id,
                'imdb_url': f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else None
            }
        
        return {'poster': None, 'imdb_id': None, 'imdb_url': None}
    except:
        return {'poster': None, 'imdb_id': None, 'imdb_url': None}

def get_fallback_poster(movie_title):
    """Generate fallback poster"""
    encoded_title = quote(movie_title)
    return f"https://via.placeholder.com/500x750/1a1a1a/ffffff?text={encoded_title}"

@st.cache_data
def fetch_poster_combined(movie_title):
    """Get movie data with fallback"""
    movie_data = fetch_movie_data_omdb(movie_title)
    if movie_data['poster']:
        return movie_data
    
    return {
        'poster': get_fallback_poster(movie_title),
        'imdb_id': None,
        'imdb_url': None
    }

def recommend(movie):
    """Recommend movies and fetch data"""
    movie_idx = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_idx]
    
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    
    recommend_movies = []
    for i in movies_list:
        movie_index = i[0]
        movie_title = movies.iloc[movie_index].title
        recommend_movies.append(movie_title)
    
    recommend_posters = []
    recommend_imdb_urls = []
    
    def fetch_single_movie_data(movie_title):
        return fetch_poster_combined(movie_title)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        movie_data_list = list(executor.map(fetch_single_movie_data, recommend_movies))
    
    for movie_data in movie_data_list:
        recommend_posters.append(movie_data['poster'])
        recommend_imdb_urls.append(movie_data['imdb_url'])
    
    return recommend_movies, recommend_posters, recommend_imdb_urls

# UI
movies_list = movies['title'].values
selected_movie = st.selectbox("Choose a movie:", movies_list)

if st.button('Recommend'):
    with st.spinner('Finding recommendations...'):
        recommendations, posters, imdb_urls = recommend(selected_movie)
    
    st.success(f"Movies similar to '{selected_movie}':")
    
    # Grid layout
    cols = st.columns(3)
    
    for idx, (movie, poster, imdb_url) in enumerate(zip(recommendations, posters, imdb_urls)):
        with cols[idx % 3]:
            try:
                st.image(poster, width=200)
                st.markdown(f"**{fix_movie_title(movie)}**")
            except:
                st.markdown(f"**{fix_movie_title(movie)}**")
                st.write("_(Poster not available)_")
    
    # Detailed view
    st.write("---")
    st.write("### More About Recommended Movies:")
    
    for idx, (movie, poster, imdb_url) in enumerate(zip(recommendations, posters, imdb_urls), 1):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            try:
                st.image(poster, width=150)
            except:
                st.write("🎭")
        
        with col2:
            display_title = fix_movie_title(movie)
            st.write(f"**{idx}. {display_title}**")
            
            if imdb_url:
                st.markdown(f"[View on IMDb]({imdb_url})")
            else:
                search_title = display_title.replace(' ', '+')
                fallback_url = f"https://www.imdb.com/find?q={search_title}&ref_=nv_sr_sm"
                st.markdown(f"[Search on IMDb]({fallback_url})")
            st.write("---")








