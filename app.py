import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=b46c067dd165e2b1986e8ab53876401c&language=en-US'
    response = requests.get(url)
    
    # Process the response as needed
    if response.status_code == 200:
        movie_data = response.json()
        # Access the movie data and retrieve the poster URL or perform other operations
        return "https://image.tmdb.org/t/p/w500/" + movie_data['poster_path']
    else:
        print('Error:', response.status_code)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        #fetch poster from api
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies,recommend_movies_posters

movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Please Type/Select a movie name',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    columns = st.columns(5)
    for i in range(5):
        if posters[i]:
            with columns[i]:
                st.text(names[i])
                st.image(posters[i])
        else:
            with columns[i]:
                st.write(names[i])
                st.write("No poster available")
# Repeat for the remaining columns...

    # col1, col2, col3, col4, col5= st.beta_columns(5)
    # with col1:
    #     st.header(names[0])
    #     st.image(posters[0])
    # with col2:
    #     st.header(names[1])
    #     st.image(posters[1])
    # with col3:
    #     st.header(names[2])
    #     st.image(posters[2])
    # with col4:
    #     st.header(names[3])
    #     st.image(posters[3])
    # with col5:
    #     st.header(names[4])
    #     st.image(posters[4])
