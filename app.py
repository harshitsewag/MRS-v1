import pickle
import streamlit as st
import requests

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/150"
    description = data.get('overview', 'No description available.')
    release_date = data.get('release_date', 'Unknown release date')
    release_year = release_date.split("-")[0] if release_date != 'Unknown release date' else 'Unknown'
    rating = data.get('vote_average', 'No rating')
    genres = ', '.join([genre['name'] for genre in data.get('genres', [])])
    duration = f"{data.get('runtime', 'N/A')} min"
    movie_url = f"https://www.themoviedb.org/movie/{movie_id}"
    return full_path, description, release_year, rating, genres, duration, movie_url

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_descriptions = []
    recommended_movie_release_years = []
    recommended_movie_ratings = []
    recommended_movie_genres = []
    recommended_movie_durations = []
    recommended_movie_urls = []
    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, description, release_year, rating, genres, duration, movie_url = fetch_movie_details(movie_id)
        recommended_movie_posters.append(poster)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_descriptions.append(description)
        recommended_movie_release_years.append(release_year)
        recommended_movie_ratings.append(rating)
        recommended_movie_genres.append(genres)
        recommended_movie_durations.append(duration)
        recommended_movie_urls.append(movie_url)

    return (recommended_movie_names, recommended_movie_posters, 
            recommended_movie_descriptions, recommended_movie_release_years, 
            recommended_movie_ratings, recommended_movie_genres, 
            recommended_movie_durations, recommended_movie_urls)

# Load the movie list and similarity matrix
movies = pickle.load(open('Artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('Artifacts/similarity.pkl', 'rb'))

# Streamlit app
st.title("Movie Recommendation System")
st.write('Using Machine Learning to recommend movies based on your preferences.')

# User input for movie selection
selected_movie = st.selectbox("Select a movie you like:", movies['title'].values)

# Number of recommendations
num_recommendations = st.slider('Number of recommendations', 1, 10, 5)

# Display recommendations
if st.button('Recommend'):
    names, posters, descriptions, release_years, ratings, genres, durations, urls = recommend(selected_movie)
    st.write(f"Top {num_recommendations} recommendations for {selected_movie}:")

    for i in range(num_recommendations):
        st.image(posters[i], width=150)
        st.write(f"**{names[i]}**")
        st.write(f"**Year:** {release_years[i]}")
        st.write(f"**Rating:** {ratings[i]}")
        st.write(f"**Genre:** {genres[i]}")
        st.write(f"**Duration:** {durations[i]}")
        st.write(f"{descriptions[i]}")
        st.write(f"[More Info]({urls[i]})")
        st.write("---")