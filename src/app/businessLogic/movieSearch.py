import requests
from themoviedb import TMDb
from justwatch import JustWatch

tmdb = TMDb(key='17766171d7b3067ced648bfe2ddc2a09')

showFinder = JustWatch(country='US')

'''
Gets the current most popular tv shows and movies
:return: popular tv shows and movies
'''
def get_popular():
    popular_tv_shows = tmdb.trending().tv_weekly().results
    popular_movies = tmdb.trending().movie_weekly().results
    popular_movies = popular_movies
    popular_tv_shows = popular_tv_shows
    return popular_movies, popular_tv_shows


'''
Gets the name of the show or movie from its id
:param id: the id of the movie or show
:param media_type: movie or tv
:return: true if they match, false if they don't
'''
def get_name(id, media_type):
    if media_type == 'tv':
        move_show = tmdb.tv(id).details()
        return move_show.name
    elif media_type == 'movie':
        move_show = tmdb.movie(id).details()
        return move_show.title
    else:
        return '[Failed To Load :(]'


'''
Searches for the movie or tv show
:param query: the query for the API
:param hashed_password_from_db: the stored hashed password in the database
:return: results of the search
'''
def search_movies_and_tv_shows(query):
    url = 'https://api.themoviedb.org/3/search/multi'
    params = {
        'include_adult': 'false',
        'language': 'en-US',
        'page': 1,
        'query': query,
        'api_key': '17766171d7b3067ced648bfe2ddc2a09',  # Replace with your TMDb API key
    }

    headers = {
        'Accept': 'application/json',
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            formatted_results = []

            for result in data['results']:
                if result['media_type'] in ['movie', 'tv']:
                    formatted_result = {
                        'id': result['id'],
                        'title': result['title'] if result['media_type'] == 'movie' else result['name'],
                        'media_type': result['media_type'],
                        'overview': result['overview'],
                        'release_date': result['release_date'] if result['media_type'] == 'movie' else None,
                        'poster_path': result['poster_path']
                    }
                    formatted_results.append(formatted_result)

            return formatted_results
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Error while searching movies and TV shows: {str(e)}")
        return []
