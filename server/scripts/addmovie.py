from api.models import Movie
import pandas as pd
import numpy as np
import datetime
import os

def run():
    path = os.path.join(os.path.dirname(__file__), "../movie.csv")
    movies = pd.read_csv(path)
    movies['poster_path'] = movies['poster_path'].apply(lambda x: 'https://image.tmdb.org/t/p/original/' + x if x is not np.nan else x)
    movies['poster_path'].fillna('https://movieeo.com/no-poster.png', inplace=True)

    movies['release_date'].fillna(str("1-1-2023"), inplace=True)
    movies.fillna(0, inplace=True)
    movies.drop_duplicates(subset='title', keep='first', inplace=True)
    movies.drop_duplicates(subset='id', keep='first', inplace=True)
    movies.dropna(how='all',inplace=True)
    movies['runtime'] = movies['runtime'].astype(int)
    # print(movies.info())
    # print(movies.isnull().sum())
    dates=[]
    for row in movies['release_date']:
        row = datetime.datetime.strptime(row, "%d-%m-%Y").strftime("%Y-%m-%d")
        dates.append(row)
    
    movies['release_date'] = dates

    objs = [Movie(
        id = row[1],
        title = row[2],
        vote_average=row[14],
        status=row[12],
        release_date=row[8],
        revenue=row[10],
        runtime=row[11],
        budget=row[9],
        overview=row[5],
        popularity=row[6],
        poster_path=row[18],
        tagline=row[13],
        genres=row[3],
        production_companies=row[7],
        spoken_languages=row[4],
        credit=row[16],
        keywords=row[17]
        ) for row in movies.itertuples()]
    print("updating database...")
    for obj in objs:
        try:
            Movie.objects.update_or_create(
            id=obj.id,
            defaults={
                'title':obj.title,
                'vote_average':obj.vote_average,
                'status':obj.status,
                'release_date':obj.release_date,
                'revenue':obj.revenue,
                'runtime':obj.runtime,
                'budget':obj.budget,
                'overview':obj.overview,
                'popularity':obj.popularity,
                'poster_path':obj.poster_path,
                'tagline':obj.tagline,
                'genres':obj.genres,
                'production_companies':obj.production_companies,
                'spoken_languages':obj.spoken_languages,
                'credit':obj.credit,
                'keywords':obj.keywords
                }
            )
        except Exception as e:
            print(obj)
    print("database updated")
