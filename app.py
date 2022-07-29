import streamlit as st
import pandas as pd
import pickle
import requests
import gzip

# import numpy as np

st.title("Movie Recommendation System")
st.markdown("Hey there! I am a movie recommendation system. I can help you find movies that you might like.")

movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

# similarity = pickle.load(open("similarity.pkl", "rb"))
similarity = pickle.load(gzip.open("similarity_gzip.pgz", "rb"))
    

def fetch_poster(movie_id):
   res = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=86ba31f4f2b7c32ec0d12d3a352bf8a1".format(movie_id))
   data = res.json()
   return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    
    

def recommend(movie): 
     # finding movie index in the dataframe
    movie_index = movies[movies['title'] == movie].index[0]
    # Picking the top 5 similar movies
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x : x[1])[1:6]
    
    recommend_movies =[]
    recommend_movies_posters = []
    for i in movies_list: 
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters


selected_movie = st.selectbox("Select a Movie", movies['title'].values)


if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    j = 0
    for i in st.columns(5):
      with i:
        st.text(names[j])
        st.image(posters[j])
        j += 1
  


