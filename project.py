import json
import requests_with_caching

def get_movies_from_tastedive(movie):
    """Return the list of related movies as given one."""
    base = 'https://tastedive.com/api/similar'
    payload = {'q': movie,
               'type': 'movies',
               'limit': 5}
    response = requests_with_caching.get(base, params=payload)
    movies_dict = json.loads(response.text)
    return movies_dict

def extract_movie_titles(movies):
    # extract the name from movies dictionary.
    return [movie['Name'] for movie in movies['Similar']['Results']]

def get_related_titles(movie_lst):
    related_lst = []
    for movie in movie_lst:
        related_movies = get_movies_from_tastedive(movie)
        for name in extract_movie_titles(related_movies):
            if name not in related_lst:
                related_lst.append(name)
    return related_lst

def get_movie_data(title):
    base = 'http://www.omdbapi.com/'
    payload = {'t': title,
               'r': 'json'}
    
    response = requests_with_caching.get(base, params=payload)
    return json.loads(response.text)

def get_movie_rating(movie_info):
    ratings = movie_info['Ratings']
    for rating in ratings:
        if rating['Source'] == 'Rotten Tomatoes':
            return int(rating['Value'][:-1])
    return 0
def get_sorted_recommendations(movie_titles):
    rated_movie = {}
    related_movie = get_related_titles(movie_titles)
    for movie in related_movie:
        movie_info = get_movie_data(movie)
        rated_movie[movie] = get_movie_rating(movie_info)
    
    rated_names = list(rated_movie.items())
    for _ in range(len(rated_names)):
        for i in range(len(rated_names) - 1):
            if rated_names[i][1] < rated_names[i+1][1]:
                rated_names[i], rated_names[i+1] = rated_names[i+1], rated_names[i]

    return[name[0] for name in rated_names]
    
    
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])

