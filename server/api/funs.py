import json
import ast
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import linear_kernel,cosine_similarity
import requests
from .models import *
from django.forms.models import model_to_dict
import os
api_key = '3c82ec187c6088eb5840b98740de3c09'


def search_similar_movies(movie_id):
    
    df = pd.DataFrame(list(Movie.objects.all().values()))
    
    df['text_combined'] = (
        df['genres'].apply(lambda x: x.replace('-',' ')) + ' ' +
        df['production_companies'].apply(lambda x:x.replace(' ','').replace('-',' ').lower()) + ' ' +
        df['title'].apply(lambda x: x.replace(' ','')) + ' ' +
        df['keywords'].apply(lambda x: x.replace('-',' ').lower()) + ' ' +
        df['credit'].apply(lambda x: x.replace(' ','').replace('-',' ').lower())
    )
    current_movie = df[df['id'] == int(movie_id)]
    feature = (
        current_movie['genres'].apply(lambda x: x.replace('-',' ')) + ' ' +
        current_movie['production_companies'].apply(lambda x:x.replace(' ','').replace('-',' ').lower()) + ' ' +
        current_movie['title'].apply(lambda x: x.replace(' ','')) + ' ' +
        current_movie['keywords'].apply(lambda x: x.replace('-',' ').lower()) + ' ' +
        current_movie['credit'].apply(lambda x: x.replace(' ','').replace('-',' ').lower())
    )
    
    # TF-IDF vectorization with adjusted weights
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    tfidf_matrix = tfidf_vectorizer.fit_transform(df['text_combined'])
    current_vector = tfidf_vectorizer.transform([feature.values[0]])

    # Calculate cosine similarities
    cosine_similarities = cosine_similarity(current_vector, tfidf_matrix).flatten()
    df['similarity'] = cosine_similarities

    similar_movies = df[df['id'] != int(movie_id)].sort_values(by='similarity', ascending=False).head(10)
    movie = current_movie.to_dict(orient='records')

    if movie[0]['genres'] is not None:
        movie[0]['genres'] = movie[0]['genres'].split('-')
    if movie[0]['production_companies'] is not None:
        movie[0]['production_companies'] = movie[0]['production_companies'].split('-')
    if movie[0]['credit'] is not None:
        movie[0]['credit'] = movie[0]['credit'].split('-')
    if movie[0]['keywords'] is not None:
        movie[0]['keywords'] = movie[0]['keywords'].split('-')
    return {
        'movie': movie[0],
        'recommendations': similar_movies.to_dict(orient='records')
    }


def watch_recommend(user):
    movie_data = pd.DataFrame(list(Movie.objects.all().values()))

    print(movie_data.info())
    # Combine features into a single text feature
    movie_data['combined_features'] = (
        movie_data['title'] + ' ' +
        movie_data['genres'] + ' ' +
        movie_data['production_companies'] + ' ' +
        movie_data['keywords'] + ' ' +
        movie_data['credit']
    )

    
    # Use CountVectorizer for text feature extraction
    count_vectorizer = CountVectorizer(stop_words='english')
    feature_matrix = count_vectorizer.fit_transform(movie_data['combined_features'])

    # Calculate cosine similarity
    cosine_similarity_matrix = cosine_similarity(feature_matrix, feature_matrix)

    # Function to recommend movies based on recently watched movies
    def recommend_movies(recently_watched_movies):
        # Combine features of recently watched movies
        recently_watched_combined_features = [
            ' '.join([movie.movie.title, movie.movie.genres, movie.movie.production_companies, movie.movie.keywords, movie.movie.credit])
            for movie in recently_watched_movies
        ]

        # Transform recently watched movies using the same CountVectorizer
        recently_watched_feature_matrix = count_vectorizer.transform(recently_watched_combined_features)

        # Calculate cosine similarity between recently watched and all movies
        similarity_scores = cosine_similarity(recently_watched_feature_matrix, feature_matrix)

        # Get indices of recommended movies based on highest similarity
        recommended_movie_indices = similarity_scores.mean(axis=0).argsort()[::-1]

        # Display recommended movies
        recommendations = movie_data.iloc[recommended_movie_indices[:30]].to_dict(orient='records')

        return recommendations
    
    watched  = WatchHistory.objects.filter(user=user).order_by('-added')[:15]
    recommendations = recommend_movies(watched)
    movies = []
    
    for movie in recommendations:
        m = Movie.objects.get(id=movie['id'])
        m.isFavorite = Favorite.objects.filter(user=user,movie=m).exists()
        movies.append(model_to_dict(m))
    return movies