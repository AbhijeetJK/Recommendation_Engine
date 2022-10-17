import streamlit as st
import pickle as pl
import pandas as pd
import requests
page_bg_img = '''
<style>
body {
background-image: url("");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)
movies_releas_year = ''
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=32fcfd6663ea899305351d709feb33c0&language=en-US".format(movie_id)
    print(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    print("hi")
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

    return full_path






def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

def People_recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[6:12]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters








st.title('Movie Recomandations System')
movie_list = pl.load(open('C:\\Users\\hp\\PycharmProjects\\untitled4\\Recomandation_System\\movie.pkl','rb'))
movies = pd.DataFrame(movie_list)
similarity = pl.load(open('C:\\Users\\hp\\PycharmProjects\\untitled4\\Recomandation_System\\similarity.pkl','rb'))


def year_wise_recommend(movie):
    global movies_releas_year
    movies_releas_year = list(movies[movies['title'] == movie]['release_date'])
    movies_releas_date = list(movies['release_date'])
    movie_title = list(movies['id'])
    Top_five_movies = []
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_releas_date:
        if i == movies_releas_year[0]:
            Top_five_movies.append(movies[(movies['release_date']==i) & (movies['vote_average'] >= 7.4 ) & (movies['title'] != movie ) ]['id'])
        if len(Top_five_movies) == 1:
            break
    flatList = [item for k in Top_five_movies for item in k]
    for j in flatList:
        recommended_movie_names.append(movies[movies['id'] == j]['title'])
    recommended_movie_names  = [m for k in recommended_movie_names for m in k]

    for k in flatList:
        recommended_movie_posters.append(fetch_poster(k))

    return recommended_movie_names, recommended_movie_posters


selected_movie = st.selectbox(
    "Select movie name",
    movies['title'].values
)



if st.button('Show Movies'):
    names,poster = recommend(selected_movie)
    st.header('Recommend for you')
    col1, col2, col3, col4, col5 = st.beta_columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])

    st.header('People Also Like')
    p_name, p_poster = People_recommend(selected_movie)
    col9, col10, col11= st.beta_columns(3)
    with col9:
        st.text(p_name[0])
        st.image(p_poster[0])
    with col10:
        st.text(p_name[1])
        st.image(p_poster[1])
    with col11:
        st.text(p_name[2])
        st.image(p_poster[2])



    st.header('Most Rated Movies in Same year')
    m_name , m_poster = year_wise_recommend(selected_movie)
    col6, col7,col8 = st.beta_columns(3)
    with col6:
        st.text(m_name[0])
        st.image(m_poster[0])
    with col7:
        st.text(m_name[1])
        st.image(m_poster[1])
    with col8:
        st.text(m_name[2])
        st.image(m_poster[2])
