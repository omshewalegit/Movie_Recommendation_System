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


# # import streamlit as st
# # import pickle
# # import pandas as pd
# # import requests
# # from urllib.parse import quote
# # import time

# # # Load data
# # movies = pickle.load(open('movies.pkl','rb'))
# # similarity = pickle.load(open('similarity.pkl','rb'))

# # st.title('Movie Recommender System 🎬')

# # # OPTION 1: Using OMDb API with your API key
# # def fetch_poster_omdb(movie_title):
# #     """
# #     Fetch movie poster from OMDb API using your API key
# #     """
# #     try:
# #         # Your OMDb API key
# #         api_key = "81293116"
        
# #         # Clean the movie title for URL
# #         clean_title = quote(movie_title.strip())
# #         url = f"http://www.omdbapi.com/?apikey={api_key}&t={clean_title}&plot=short&r=json"
        
# #         response = requests.get(url)
# #         data = response.json()
        
# #         if response.status_code == 200 and data.get('Response') == 'True':
# #             poster_url = data.get('Poster')
# #             if poster_url and poster_url != 'N/A':
# #                 return poster_url
        
# #         return None
# #     except Exception as e:
# #         print(f"Error fetching poster from OMDb for '{movie_title}': {e}")
# #         return None

# # # OPTION 2: Using TMDB without API key (Web scraping approach)
# # def fetch_poster_tmdb_scrape(movie_title):
# #     """
# #     Search TMDB website directly (no API key needed)
# #     """
# #     try:
# #         # This is a simplified approach - in production, you'd want more robust scraping
# #         search_query = quote(movie_title.replace(' ', '+'))
# #         # Note: This is a basic example. For production use, consider using BeautifulSoup
# #         return None  # Placeholder - web scraping can be complex and may violate terms of service
# #     except:
# #         return None

# # # OPTION 3: Using a fallback poster database
# # def get_fallback_poster(movie_title):
# #     """
# #     Generate a custom poster with movie title
# #     """
# #     # Create a placeholder URL with the movie title
# #     encoded_title = quote(movie_title)
# #     return f"https://via.placeholder.com/500x750/1a1a1a/ffffff?text={encoded_title}"

# # # OPTION 4: Using local poster images (if you have them)
# # def get_local_poster(movie_title):
# #     """
# #     Use local poster images if available
# #     """
# #     # Assuming you have a folder called 'posters' with movie poster images
# #     # Image names should match movie titles (with proper file extensions)
# #     try:
# #         # Clean filename
# #         filename = movie_title.replace(' ', '_').replace(':', '').replace('?', '').lower()
# #         possible_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        
# #         for ext in possible_extensions:
# #             poster_path = f"posters/{filename}{ext}"
# #             # In a real implementation, you'd check if file exists
# #             # For now, return None to use fallback
# #             pass
        
# #         return None
# #     except:
# #         return None

# # # OPTION 5: Combined approach - try multiple sources
# # @st.cache_data
# # def fetch_poster_combined(movie_title):
# #     """
# #     Try multiple methods to get movie poster
# #     """
# #     # Method 1: Try OMDb API
# #     poster_url = fetch_poster_omdb(movie_title)
# #     if poster_url:
# #         return poster_url
    
# #     # Method 2: Try local posters
# #     poster_url = get_local_poster(movie_title)
# #     if poster_url:
# #         return poster_url
    
# #     # Method 3: Use fallback with movie title
# #     return get_fallback_poster(movie_title)

# # def recommend(movie):
# #     """
# #     Recommend movies based on similarity and fetch their posters
# #     """
# #     recommend_movies = []
# #     recommend_posters = []
    
# #     # Find the index of the selected movie
# #     movie_idx = movies[movies['title'] == movie].index[0]
# #     distances = similarity[movie_idx]
    
# #     # Get top 10 similar movies (excluding the selected movie itself)
# #     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    
# #     for i in movies_list:
# #         movie_index = i[0]
        
# #         # Get movie title
# #         movie_title = movies.iloc[movie_index].title
# #         recommend_movies.append(movie_title)
        
# #         # Get movie poster using combined approach
# #         poster_url = fetch_poster_combined(movie_title)
# #         recommend_posters.append(poster_url)
        
# #         # Small delay to avoid overwhelming the API
# #         time.sleep(0.1)
    
# #     return recommend_movies, recommend_posters

# # # Streamlit UI
# # movies_list = movies['title'].values
# # selected_movie = st.selectbox(
# #     "Choose a movie:",
# #     movies_list
# # )

# # if st.button('Recommend'):
# #     with st.spinner('Finding recommendations and fetching posters...'):
# #         recommendations, posters = recommend(selected_movie)
    
# #     st.success(f"Movies similar to '{selected_movie}':")
    
# #     # Display recommendations in a grid layout
# #     cols = st.columns(3)  # 3 columns for better mobile responsiveness
    
# #     for idx, (movie, poster) in enumerate(zip(recommendations, posters)):
# #         with cols[idx % 3]:
# #             try:
# #                 st.image(poster, width=200, caption=movie)
# #             except:
# #                 # If image fails to load, show text only
# #                 st.write(f"🎬 **{movie}**")
# #                 st.write("_(Poster not available)_")
    
# #     # Alternative detailed view
# #     st.write("---")
# #     st.write("### Detailed Recommendations:")
    
# #     for idx, (movie, poster) in enumerate(zip(recommendations, posters), 1):
# #         col1, col2 = st.columns([1, 2])
        
# #         with col1:
# #             try:
# #                 st.image(poster, width=150)
# #             except:
# #                 st.write("🎭")  # Movie emoji as fallback
        
# #         with col2:
# #             st.write(f"**{idx}. {movie}**")
# #             st.write("Click to see more details...")
# #             st.write("---")

# # # Additional Options Information
# # with st.expander("📝 Poster Sources Info"):
# #     st.write("""
# #     **Current poster sources (in order of preference):**
    
# #     1. **OMDb API**: Free API with basic movie data
# #     2. **Local Images**: If you have poster images stored locally
# #     3. **Custom Placeholders**: Generated placeholder with movie title
    
# #     **To improve poster quality:**
# #     - Download poster images manually and place them in a 'posters' folder
# #     - Get a free OMDb API key from http://www.omdbapi.com/apikey.aspx
# #     - Use IMDb IDs if available in your dataset for better matching
# #     """)

# # # Quick Setup Guide
# # with st.expander("🚀 Quick Setup for Better Posters"):
# #     st.write("""
# #     **Option A: Get OMDb API Key (Recommended)**
# #     1. Go to http://www.omdbapi.com/apikey.aspx
# #     2. Sign up for a free account
# #     3. Get your API key
# #     4. Add it to the code: `url = f"http://www.omdbapi.com/?apikey=YOUR_KEY&t={clean_title}"`
    
# #     **Option B: Download Posters Manually**
# #     1. Create a 'posters' folder in your project directory
# #     2. Download poster images for your movies
# #     3. Name them as: movie_title.jpg (replace spaces with underscores)
    
# #     **Option C: Use Movie IDs**
# #     If your dataset has IMDb IDs, you can use them for better poster matching!
# #     """)

# # import streamlit as st
# # import pickle
# # import pandas as pd
# # import requests
# # from urllib.parse import quote
# # import time

# # # Load data
# # movies = pickle.load(open('movies.pkl','rb'))
# # similarity = pickle.load(open('similarity.pkl','rb'))

# # st.title('Movie Recommender System 🎬')

# # # Using OMDb API with your API key
# # def fetch_movie_data_omdb(movie_title):
# #     """
# #     Fetch movie data including poster and IMDb ID from OMDb API
# #     """
# #     try:
# #         # Your OMDb API key
# #         api_key = "81293116"
        
# #         # Clean the movie title for URL
# #         clean_title = quote(movie_title.strip())
# #         url = f"http://www.omdbapi.com/?apikey={api_key}&t={clean_title}&plot=short&r=json"
        
# #         response = requests.get(url)
# #         data = response.json()
        
# #         if response.status_code == 200 and data.get('Response') == 'True':
# #             poster_url = data.get('Poster')
# #             imdb_id = data.get('imdbID')
            
# #             return {
# #                 'poster': poster_url if poster_url != 'N/A' else None,
# #                 'imdb_id': imdb_id,
# #                 'imdb_url': f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else None
# #             }
        
# #         return {'poster': None, 'imdb_id': None, 'imdb_url': None}
# #     except Exception as e:
# #         print(f"Error fetching data from OMDb for '{movie_title}': {e}")
# #         return {'poster': None, 'imdb_id': None, 'imdb_url': None}

# # # OPTION 2: Using TMDB without API key (Web scraping approach)
# # def fetch_poster_tmdb_scrape(movie_title):
# #     """
# #     Search TMDB website directly (no API key needed)
# #     """
# #     try:
# #         # This is a simplified approach - in production, you'd want more robust scraping
# #         search_query = quote(movie_title.replace(' ', '+'))
# #         # Note: This is a basic example. For production use, consider using BeautifulSoup
# #         return None  # Placeholder - web scraping can be complex and may violate terms of service
# #     except:
# #         return None

# # # OPTION 3: Using a fallback poster database
# # def get_fallback_poster(movie_title):
# #     """
# #     Generate a custom poster with movie title
# #     """
# #     # Create a placeholder URL with the movie title
# #     encoded_title = quote(movie_title)
# #     return f"https://via.placeholder.com/500x750/1a1a1a/ffffff?text={encoded_title}"

# # # OPTION 4: Using local poster images (if you have them)
# # def get_local_poster(movie_title):
# #     """
# #     Use local poster images if available
# #     """
# #     # Assuming you have a folder called 'posters' with movie poster images
# #     # Image names should match movie titles (with proper file extensions)
# #     try:
# #         # Clean filename
# #         filename = movie_title.replace(' ', '_').replace(':', '').replace('?', '').lower()
# #         possible_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        
# #         for ext in possible_extensions:
# #             poster_path = f"posters/{filename}{ext}"
# #             # In a real implementation, you'd check if file exists
# #             # For now, return None to use fallback
# #             pass
        
# #         return None
# #     except:
# #         return None

# # # OPTION 5: Combined approach - try multiple sources
# # @st.cache_data
# # def fetch_poster_combined(movie_title):
# #     """
# #     Try multiple methods to get movie poster and IMDb data
# #     """
# #     # Method 1: Try OMDb API
# #     movie_data = fetch_movie_data_omdb(movie_title)
# #     if movie_data['poster']:
# #         return movie_data
    
# #     # Method 2: Try local posters
# #     poster_url = get_local_poster(movie_title)
# #     if poster_url:
# #         return {'poster': poster_url, 'imdb_id': None, 'imdb_url': None}
    
# #     # Method 3: Use fallback with movie title
# #     return {
# #         'poster': get_fallback_poster(movie_title),
# #         'imdb_id': None,
# #         'imdb_url': None
# #     }

# # def recommend(movie):
# #     """
# #     Recommend movies based on similarity and fetch their posters
# #     """
# #     recommend_movies = []
# #     recommend_posters = []
# #     recommend_imdb_urls = []
    
# #     # Find the index of the selected movie
# #     movie_idx = movies[movies['title'] == movie].index[0]
# #     distances = similarity[movie_idx]
    
# #     # Get top 10 similar movies (excluding the selected movie itself)
# #     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    
# #     for i in movies_list:
# #         movie_index = i[0]
        
# #         # Get movie title
# #         movie_title = movies.iloc[movie_index].title
# #         recommend_movies.append(movie_title)
        
# #         # Get movie poster and IMDb data using combined approach
# #         movie_data = fetch_poster_combined(movie_title)
# #         recommend_posters.append(movie_data['poster'])
# #         recommend_imdb_urls.append(movie_data['imdb_url'])
        
# #         # Small delay to avoid overwhelming the API
# #         time.sleep(0.1)
    
# #     return recommend_movies, recommend_posters, recommend_imdb_urls

# # # Streamlit UI
# # movies_list = movies['title'].values
# # selected_movie = st.selectbox(
# #     "Choose a movie:",
# #     movies_list
# # )

# # if st.button('Recommend'):
# #     with st.spinner('Finding recommendations and fetching posters...'):
# #         recommendations, posters, imdb_urls = recommend(selected_movie)
    
# #     st.success(f"Movies similar to '{selected_movie}':")
    
# #     # Display recommendations in a grid layout
# #     cols = st.columns(3)  # 3 columns for better mobile responsiveness
    
# #     for idx, (movie, poster, imdb_url) in enumerate(zip(recommendations, posters, imdb_urls)):
# #         with cols[idx % 3]:
# #             try:
# #                 st.image(poster, width=200, caption=movie)
# #             except:
# #                 # If image fails to load, show text only
# #                 st.write(f"🎬 **{movie}**")
# #                 st.write("_(Poster not available)_")
    
# #     # Alternative detailed view
# #     st.write("---")
# #     st.write("Recommended Movies:")
    
# #     for idx, (movie, poster, imdb_url) in enumerate(zip(recommendations, posters, imdb_urls), 1):
# #         col1, col2 = st.columns([1, 2])
        
# #         with col1:
# #             try:
# #                 st.image(poster, width=150)
# #             except:
# #                 st.write("🎭")  # Movie emoji as fallback
        
# #         with col2:
# #             st.write(f"**{idx}. {movie}**")
# #             if imdb_url:
# #                 st.markdown(f"[View on IMDb]({imdb_url})")
# #             else:
# #                 st.write("IMDb link not available")
# #             st.write("---")

# import streamlit as st
# import pickle
# import pandas as pd
# import requests
# from urllib.parse import quote
# from concurrent.futures import ThreadPoolExecutor
# import threading

# # Load data
# movies = pickle.load(open('movies.pkl','rb'))
# similarity = pickle.load(open('similarity.pkl','rb'))

# st.title('Movie Recommendation System🎬')

# # Using OMDb API with your API key - optimized version
# def fetch_movie_data_omdb(movie_title):
#     """
#     Fetch movie data including poster and IMDb ID from OMDb API
#     """
#     try:
#         # Your OMDb API key
#         api_key = "81293116"
        
#         # Clean the movie title for URL
#         clean_title = quote(movie_title.strip())
#         url = f"http://www.omdbapi.com/?apikey={api_key}&t={clean_title}&plot=short&r=json"
        
#         # Faster timeout for quicker response
#         response = requests.get(url, timeout=2)
#         data = response.json()
        
#         if response.status_code == 200 and data.get('Response') == 'True':
#             poster_url = data.get('Poster')
#             imdb_id = data.get('imdbID')
            
#             return {
#                 'poster': poster_url if poster_url != 'N/A' else None,
#                 'imdb_id': imdb_id,
#                 'imdb_url': f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else None
#             }
        
#         return {'poster': None, 'imdb_id': None, 'imdb_url': None}
#     except:
#         # Quick fallback without detailed error handling for speed
#         return {'poster': None, 'imdb_id': None, 'imdb_url': None}

# # OPTION 2: Using TMDB without API key (Web scraping approach)
# def fetch_poster_tmdb_scrape(movie_title):
#     """
#     Search TMDB website directly (no API key needed)
#     """
#     try:
#         # This is a simplified approach - in production, you'd want more robust scraping
#         search_query = quote(movie_title.replace(' ', '+'))
#         # Note: This is a basic example. For production use, consider using BeautifulSoup
#         return None  # Placeholder - web scraping can be complex and may violate terms of service
#     except:
#         return None

# # OPTION 3: Using a fallback poster database
# def get_fallback_poster(movie_title):
#     """
#     Generate a custom poster with movie title
#     """
#     # Create a placeholder URL with the movie title
#     encoded_title = quote(movie_title)
#     return f"https://via.placeholder.com/500x750/1a1a1a/ffffff?text={encoded_title}"

# # OPTION 4: Using local poster images (if you have them)
# def get_local_poster(movie_title):
#     """
#     Use local poster images if available
#     """
#     # Assuming you have a folder called 'posters' with movie poster images
#     # Image names should match movie titles (with proper file extensions)
#     try:
#         # Clean filename
#         filename = movie_title.replace(' ', '_').replace(':', '').replace('?', '').lower()
#         possible_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        
#         for ext in possible_extensions:
#             poster_path = f"posters/{filename}{ext}"
#             # In a real implementation, you'd check if file exists
#             # For now, return None to use fallback
#             pass
        
#         return None
#     except:
#         return None

# # OPTION 5: Combined approach - try multiple sources
# @st.cache_data
# def fetch_poster_combined(movie_title):
#     """
#     Try multiple methods to get movie poster and IMDb data
#     """
#     # Method 1: Try OMDb API
#     movie_data = fetch_movie_data_omdb(movie_title)
#     if movie_data['poster']:
#         return movie_data
    
#     # Method 2: Try local posters
#     poster_url = get_local_poster(movie_title)
#     if poster_url:
#         return {'poster': poster_url, 'imdb_id': None, 'imdb_url': None}
    
#     # Method 3: Use fallback with movie title
#     return {
#         'poster': get_fallback_poster(movie_title),
#         'imdb_id': None,
#         'imdb_url': None
#     }

# def recommend(movie):
#     """
#     Recommend movies based on similarity and fetch their posters - SUPER FAST VERSION
#     """
#     # Find the index of the selected movie
#     movie_idx = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_idx]
    
#     # Get top 10 similar movies (excluding the selected movie itself)
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    
#     # Get all movie titles first
#     recommend_movies = []
#     for i in movies_list:
#         movie_index = i[0]
#         movie_title = movies.iloc[movie_index].title
#         recommend_movies.append(movie_title)
    
#     # Use ThreadPoolExecutor for parallel API calls - MUCH FASTER!
#     recommend_posters = []
#     recommend_imdb_urls = []
    
#     def fetch_single_movie_data(movie_title):
#         return fetch_poster_combined(movie_title)
    
#     # Fetch all movie data in parallel (up to 5 threads)
#     with ThreadPoolExecutor(max_workers=5) as executor:
#         movie_data_list = list(executor.map(fetch_single_movie_data, recommend_movies))
    
#     # Extract posters and URLs
#     for movie_data in movie_data_list:
#         recommend_posters.append(movie_data['poster'])
#         recommend_imdb_urls.append(movie_data['imdb_url'])
    
#     return recommend_movies, recommend_posters, recommend_imdb_urls

# # Streamlit UI
# movies_list = movies['title'].values
# selected_movie = st.selectbox(
#     "Choose a movie:",
#     movies_list
# )

# if st.button('Recommend'):
#     with st.spinner('Finding recommendations and fetching posters...'):
#         recommendations, posters, imdb_urls = recommend(selected_movie)
    
#     st.success(f"Movies similar to '{selected_movie}':")
    
#     # Display recommendations in a grid layout
#     cols = st.columns(3)  # 3 columns for better mobile responsiveness
    
#     for idx, (movie, poster, imdb_url) in enumerate(zip(recommendations, posters, imdb_urls)):
#         with cols[idx % 3]:
#             try:
#                 st.image(poster, width=200, caption=movie)
#             except:
#                 # If image fails to load, show text only
#                 st.write(f"🎬 **{movie}**")
#                 st.write("_(Poster not available)_")
    
#     # Alternative detailed view
#     st.write("---")
#     st.write("### 🎬 Recommended Movies:")
    
#     for idx, (movie, poster, imdb_url) in enumerate(zip(recommendations, posters, imdb_urls), 1):
#         col1, col2 = st.columns([1, 2])
        
#         with col1:
#             try:
#                 st.image(poster, width=150)
#             except:
#                 st.write("🎭")  # Movie emoji as fallback
        
#         with col2:
#             st.write(f"**{idx}. {movie}**")
#             if imdb_url:
#                 st.markdown(f"[View on IMDb]({imdb_url})")
#             else:
#                 st.write("IMDb link not available")
#             st.write("---")

# 


import streamlit as st
import pandas as pd
import requests
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title('Movie Recommendation System🎬')

# Load and process data directly from CSV
@st.cache_data
def load_and_process_data():
    """Load movies data and create similarity matrix"""
    try:
        # Load the movies CSV file
        movies = pd.read_csv('movies.csv')
        
        # Basic preprocessing - you might need to adjust this based on your CSV structure
        # Assuming your CSV has columns like 'title', 'genres', 'overview', etc.
        
        # If you have a 'tags' or 'features' column, use that
        if 'tags' in movies.columns:
            features = movies['tags'].fillna('')
        elif 'overview' in movies.columns:
            features = movies['overview'].fillna('')
        elif 'genres' in movies.columns:
            features = movies['genres'].fillna('')
        else:
            # Fallback: use title
            features = movies['title'].fillna('')
        
        # Create similarity matrix
        cv = CountVectorizer(max_features=5000, stop_words='english')
        vectors = cv.fit_transform(features).toarray()
        similarity = cosine_similarity(vectors)
        
        return movies, similarity
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

# Load data
movies, similarity = load_and_process_data()

if movies is None:
    st.error("Could not load movie data. Please check if 'movies.csv' exists in your repository.")
    st.stop()

# Using OMDb API with your API key - optimized version
def fetch_movie_data_omdb(movie_title):
    """
    Fetch movie data including poster and IMDb ID from OMDb API
    """
    try:
        # Your OMDb API key
        api_key = "81293116"
        
        # Clean the movie title for URL
        clean_title = quote(movie_title.strip())
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={clean_title}&plot=short&r=json"
        
        # Faster timeout for quicker response
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
        # Quick fallback without detailed error handling for speed
        return {'poster': None, 'imdb_id': None, 'imdb_url': None}

# Using a fallback poster database
def get_fallback_poster(movie_title):
    """
    Generate a custom poster with movie title
    """
    # Create a placeholder URL with the movie title
    encoded_title = quote(movie_title)
    return f"https://via.placeholder.com/500x750/1a1a1a/ffffff?text={encoded_title}"

# Combined approach - try multiple sources
@st.cache_data
def fetch_poster_combined(movie_title):
    """
    Try multiple methods to get movie poster and IMDb data
    """
    # Method 1: Try OMDb API
    movie_data = fetch_movie_data_omdb(movie_title)
    if movie_data['poster']:
        return movie_data
    
    # Method 2: Use fallback with movie title
    return {
        'poster': get_fallback_poster(movie_title),
        'imdb_id': None,
        'imdb_url': None
    }

def recommend(movie):
    """
    Recommend movies based on similarity and fetch their posters - SUPER FAST VERSION
    """
    # Find the index of the selected movie
    movie_idx = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_idx]
    
    # Get top 10 similar movies (excluding the selected movie itself)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    
    # Get all movie titles first
    recommend_movies = []
    for i in movies_list:
        movie_index = i[0]
        movie_title = movies.iloc[movie_index].title
        recommend_movies.append(movie_title)
    
    # Use ThreadPoolExecutor for parallel API calls - MUCH FASTER!
    recommend_posters = []
    recommend_imdb_urls = []
    
    def fetch_single_movie_data(movie_title):
        return fetch_poster_combined(movie_title)
    
    # Fetch all movie data in parallel (up to 5 threads)
    with ThreadPoolExecutor(max_workers=5) as executor:
        movie_data_list = list(executor.map(fetch_single_movie_data, recommend_movies))
    
    # Extract posters and URLs
    for movie_data in movie_data_list:
        recommend_posters.append(movie_data['poster'])
        recommend_imdb_urls.append(movie_data['imdb_url'])
    
    return recommend_movies, recommend_posters, recommend_imdb_urls

# Streamlit UI
movies_list = movies['title'].values
selected_movie = st.selectbox(
    "Choose a movie:",
    movies_list
)

if st.button('Recommend'):
    with st.spinner('Finding recommendations and fetching posters...'):
        recommendations, posters, imdb_urls = recommend(selected_movie)
    
    st.success(f"Movies similar to '{selected_movie}':")
    
    # Display recommendations in a grid layout
    cols = st.columns(3)  # 3 columns for better mobile responsiveness
    
    for idx, (movie, poster, imdb_url) in enumerate(zip(recommendations, posters, imdb_urls)):
        with cols[idx % 3]:
            try:
                st.image(poster, width=200, caption=movie)
            except:
                # If image fails to load, show text only
                st.write(f"🎬 **{movie}**")
                st.write("_(Poster not available)_")
    
    # Alternative detailed view
    st.write("---")
    st.write("### 🎬 Recommended Movies:")
    
    for idx, (movie, poster, imdb_url) in enumerate(zip(recommendations, posters, imdb_urls), 1):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            try:
                st.image(poster, width=150)
            except:
                st.write("🎭")  # Movie emoji as fallback
        
        with col2:
            st.write(f"**{idx}. {movie}**")
            if imdb_url:
                st.markdown(f"[View on IMDb]({imdb_url})")
            else:
                st.write("IMDb link not available")
            st.write("---")