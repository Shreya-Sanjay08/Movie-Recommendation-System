import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the data
movies_data = pd.read_csv('movies.csv')

# Select the features
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']

# Fill missing values
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

# Combine all selected features
combined_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + \
                    movies_data['tagline'] + ' ' + movies_data['cast'] + ' ' + \
                    movies_data['director']

# Convert text to vectors
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

# Calculate cosine similarity
similarity = cosine_similarity(feature_vectors)

# Create a list of titles
movie_titles = movies_data['title'].tolist()

# Keep the existing recommend_movies() function

def get_genre_distribution(movies_data):
    all_genres = movies_data['genres'].str.split('|').explode()
    return all_genres.value_counts().head(10)


def recommend_movies(movie_name, top_n=10):
    # Find close match to movie title
    matches = difflib.get_close_matches(movie_name, movie_titles)
    if not matches:
        return []
    
    close_match = matches[0]
    movie_index = movies_data[movies_data.title == close_match].index.values[0]

    # Get list of similar movies
    scores = list(enumerate(similarity[movie_index]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    
    recommended_titles = []
    for i in sorted_scores[1:top_n+1]:  # skip the input movie itself
        index = i[0]
        title = movies_data.iloc[index]['title']
        recommended_titles.append(title)

    return recommended_titles
