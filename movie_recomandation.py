import numpy as np
import pandas as pd
import ast as at

movie_data1 = pd.read_csv('C:\\Users\\hp\\Desktop\\Recommadation_System_full_project\\tmdb_5000_movies.csv')
cast = pd.read_csv('C:\\Users\\hp\\Desktop\\Recommendation_system\\Recommadation_System_full_project\\tmdb_5000_credits.csv')

print(movie_data1.head(1))
print(cast.head(1)['cast'])
print(movie_data1.info())
print(cast.info())
print(movie_data1.shape)
print(cast.shape)

#Merage Two Data into 1
movie_data = movie_data1.merge(cast,on='title')
print(movie_data.info())
print(movie_data.shape)

# remove Unwanted Columns

movie_data = movie_data[['id','title','genres','keywords','overview','release_date','cast','crew','vote_average']]
movie_data['release_date'] = pd.to_datetime(movie_data['release_date'])
print(movie_data.info())

#drop missing data from Data frame
movie_data.dropna(inplace=True)
#check duplicate value in data frame
print(movie_data.duplicated().sum())


# Extract the relevent information from columns

def Extract_info(mov_obj):
    genres_of_movie = []
    for i in at.literal_eval(mov_obj):
        genres_of_movie.append(i['name'])
    return genres_of_movie

movie_data['genres'] = movie_data['genres'].apply(Extract_info)
#print(movie_data['genres'])

movie_data['keywords'] = movie_data['keywords'].apply(Extract_info)
#print(movie_data['keywords'])

#Extract Top 3 Hero in Cast column

def Extract_info_cast(mov_obj):
    genres_of_movie = []
    counter = 0
    for i in at.literal_eval(mov_obj):
        if counter !=3:
            genres_of_movie.append(i['name'])
            counter+=1
        else:
            break
    return genres_of_movie


movie_data['cast'] = movie_data['cast'].apply(Extract_info_cast)
#print(movie_data['cast'])
#print("Top 3 cast is",movie_data['cast'][0])

# Extract Director name from crew

def Extract_info_crew(mov_obj):
    genres_of_movie = []
    for i in at.literal_eval(mov_obj):
        if i['job'] == 'Director':
                genres_of_movie.append(i['name'])
                break
    return genres_of_movie

movie_data['crew'] = movie_data['crew'].apply(Extract_info_crew)
#print("director is ",movie_data['crew'][0])

## spliting Overview Column with word
movie_data['overview'] = movie_data['overview'].apply(lambda x:x.split())
#print("Overvire",movie_data['overview'][0])

## we will remove  spaces between 2 words in genres casr crew column

movie_data['genres'] = movie_data['genres'].apply(lambda x :[i.replace(" ","") for i in x ] )
movie_data['keywords'] = movie_data['keywords'].apply(lambda x :[i.replace(" ","") for i in x ] )
movie_data['cast'] = movie_data['cast'].apply(lambda x :[i.replace(" ","") for i in x ] )
movie_data['crew'] = movie_data['crew'].apply(lambda x :[i.replace(" ","") for i in x ] )

# concantinate all 4 string coulmn to 1
movie_data['Movie_info'] = movie_data['overview'] + movie_data['genres'] + movie_data['keywords'] + movie_data['cast'] + movie_data['crew']


movie_data['release_date'] = pd.DatetimeIndex(movie_data['release_date']).year

Movie_info = movie_data[['id','title','genres','cast','crew','vote_average','release_date']]
print(type(Movie_info['release_date']))
#creating new DF with 4 columns
movie_data_info = movie_data[['id','title','vote_average','release_date','Movie_info']]


# convert Movie info coulnm to String

movie_data_info['Movie_info'] = movie_data_info['Movie_info'].apply(lambda x:" ".join(x))

# make all word in lower case of Movie info coulmn
movie_data_info['Movie_info'] = movie_data_info['Movie_info'].apply(lambda x:x.lower())

## Now we have data with proper format now lets convert all String data into Vector using Text Vectorization Techniques.

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')

vectors = cv.fit_transform(movie_data_info['Movie_info']).toarray()
print(vectors[0])



# here we used stemming techniques of NLP
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
def stemmer(movie_info):
    y = []
    for i in movie_info.split():
        ps.stem(i)
    return " ".join(y)

movie_data_info['Movie_info'] = movie_data_info['Movie_info'].apply(stemmer)
#print(movie_data_info.info())

# here we  calculate similarity between movies using cosine similarity techniques
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)
#print(similarity)

# Now we  want to calculate first 5 movies based on user selected movie


def recommandations(movie):
    movie_pos = movie_data_info[movie_data_info['title']== movie].index[0]
    distances = similarity[movie_pos]
    recommaded_movies = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    for i in recommaded_movies:
        print(movie_data_info.iloc[i[0]].title)

'''def year_bases_recommandationes(movie):
    movies_releas_year = Movie_info[Movie_info['title']== movie]['release_date']

    movies_releas_year = list(movies_releas_year)
    Top_movies_rates = []

    counter = 0
    for i in Movie_info['release_date']:
        if i == movies_releas_year[0]:
            Top_movies_rates.append(sorted(list(Movie_info[Movie_info['release_date'] == i]['vote_average']),reverse=True,key=lambda x:x[1]))
        if len(Top_movies_rates) == 1:
            break
            
    print(Top_movies_rates)
    #Top_movies_in_year = Movie_info[Movie_info['release_date'] == movies_releas_year]['title']
    #.sprint(Top_movies_in_year)
year_bases_recommandationes('Batman Begins')'''


recommandations('Batman Begins')


# Now we have to send Movie fileto website code so that we used pickel
import pickle as pk

pk.dump(movie_data_info.to_dict(),open('C:\\Users\\hp\\PycharmProjects\\Recomandation_System\\movie.pkl','wb'))
pk.dump(similarity,open('C:\\Users\\hp\\PycharmProjects\\Recomandation_System\\similarity.pkl','wb'))


