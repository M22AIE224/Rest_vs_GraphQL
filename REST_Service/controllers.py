import requests
from flask import Flask, render_template
import time
import matplotlib.pyplot as plt

from utils import plot_movies_performance

# Define the OMDb API key and base URL
OMDB_API_KEY = '2a9f78a3'
#OMDB_API_URL = 'http://www.omdbapi.com/?i=tt3896198&apikey=2a9f78a3'
OMDB_API_URL = 'http://www.omdbapi.com'


def plot_performance_rest(num_year):
    #num_year = 5 
    plot_url = plot_movies_performance( num_year, service_call="rest")
    return render_template('performance.html', plot_url=plot_url)


###########################################################################
# Purpose:
#   Fetch movie data from the OMDb API based on the given movie title.
#
# Parameters:
#   movie_title (str): The title of the movie to search for in the OMDb database.
#
# Process:
#   Constructs a request with the movie title and API key as parameters.
#   Sends a GET request to the OMDb API and receives movie data in JSON format.
#
# Returns:
#   dict: A dictionary containing the movie data retrieved from the OMDb API.
###########################################################################
def fetch_movie_data(movie_title):
    params = {
        't': movie_title,  # 't' is the parameter for the movie title
        'apikey': OMDB_API_KEY
    }
    response = requests.get(OMDB_API_URL, params=params)
    return response.json()  # Parse JSON response


###########################################################################
# Purpose:
#   Fetch a list of movies released in a specified year from the OMDb API.
#   This function handles paginated results, processes the movie data, and 
#   tracks the time taken for the fetch operation.
#
# Parameters:
#   year (str): The year of movie releases to search for, passed as a query parameter.
#
# Process:
#   - Initializes an empty list `movie_items` to store the fetched movie data.
#   - Iterates over multiple pages of the OMDb API response using a `while` loop:
#       - Sends a GET request to the OMDb API with the specified search term (`movie`), 
#         year (`y`), and API key.
#       - For each page, retrieves the list of movie data (up to 10 movies per page).
#       - For each movie, extracts key details like title, year, genre, director, actors, 
#         plot, language, country, awards, ratings, and poster URL.
#       - Appends each movie's data to the `movie_items` list.
#   - Tracks the time taken to fetch all the pages.
#   - Breaks out of the loop if the API response indicates no more data.
#
# Returns:
#   tuple:
#     - list: A list of dictionaries, each containing movie data for a specific movie.
#     - float: The total time (in seconds) taken to fetch all the movies.
###########################################################################
def fetch_all_movies(year):
    movie_items = []
    page = 1
    search_term = "movie"
    start_time = time.time()

    while True:
        params = {
            's': search_term,
            'y': year,
            'apikey': OMDB_API_KEY,
            'page': page
        }
        response = requests.get(OMDB_API_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            if data.get("Response") == "True":
                for movie_data in data.get("Search", []):
                    movie_item = {
                        "id": movie_data.get("imdbID", "N/A"),
                        "title": movie_data.get("Title", "N/A"),
                        "year": movie_data.get("Year", "N/A"),
                        "genre": movie_data.get("Genre", "N/A").split(", "),
                        "director": movie_data.get("Director", "N/A"),
                        "actors": movie_data.get("Actors", "N/A").split(", "),
                        "plot": movie_data.get("Plot", "N/A"),
                        "language": movie_data.get("Language", "N/A"),
                        "country": movie_data.get("Country", "N/A"),
                        "awards": movie_data.get("Awards", "N/A"),
                        "ratings": [{"source": rating.get("Source"), "value": rating.get("Value")}
                                    for rating in movie_data.get("Ratings", [])],
                        "poster": movie_data.get("Poster", "N/A")
                    }
                    movie_items.append(movie_item)
            else:
                break

        page += 1

    end_time = time.time()
    time_taken = end_time - start_time

    return movie_items, time_taken


###########################################################################
# Purpose:
#   Fetch a list of movies released in a specified year from the OMDb API.
#
# Parameters:
#   year (str): The release year of the movies to fetch, passed as an argument.
#
# Process:
#   - Initializes an empty list to store movie data (`movie_items`) and sets the starting page to 1.
#   - Defines a search term ("movie") and starts a timer to track request duration.
#   - In a loop:
#       - Sends a GET request to the OMDb API with the year, search term, API key, and page number.
#       - If the response is successful, checks for movies in the "Search" field:
#           - Extracts movie details (e.g., title, year, genre, director, actors, etc.) and adds them to `movie_items`.
#       - Increments the page number to fetch the next set of movies, until no more results are returned.
#   - Calculates the total time taken for the API requests.
#
# Returns:
#   tuple: A tuple containing:
#       - movie_items (list of dict): A list of dictionaries, each with detailed movie information.
#       - time_taken (float): The time taken to fetch all movie data, in seconds.
###########################################################################
def fetch_movies_by_years(num_years):
    #years_data = []
    combined_movie_items = []
    num_years = int(num_years)
    # Ensure num_year is an integer, e.g., num_year = 5 for last 5 years
    for year in range(2024 - num_years - 1, 2024):
        movie_items, time_taken = fetch_all_movies(year)
        if movie_items:
            combined_movie_items.extend(movie_items) 
        
        #years_data.append(movie_items)
    
    return combined_movie_items


###########################################################################
# Purpose:
#   Generate and save a plot of movie counts and API request times over a range of years.
#
# Parameters:
#   num_year (int): The number of past years to include in the plot, ending in the current year.
#
# Process:
#   - Converts `num_year` to an integer and calculates a range of years ending with the current year.
#   - For each year in the range:
#       - Calls `fetch_all_movies` to retrieve movies released in that year.
#       - Counts the movies and tracks the time taken to fetch them.
#       - Appends each year's data (movie count and time taken) to `years_data`.
#   - Extracts the years, movie counts, and time taken from `years_data` for plotting.
#   - Creates a plot with:
#       - Movie counts on the left y-axis.
#       - Time taken (seconds) on the right y-axis.
#   - Saves the plot as 'rest_movies_performance.png' in the static folder.
#
# Returns:
#   str: The file path to the saved plot image.
################################################################################
def plot_movies_performance(num_year):

    num_year = int(num_year)
    years_data = []
    for year in range(2024 - num_year - 1, 2024, ):
        movie_list, time_taken = fetch_all_movies(year)
        movie_count = len(movie_list)
        fetch_performance = {
            "year": year,
            "count":movie_count,
            "time_taken": time_taken
        }
        years_data.append(fetch_performance)


    # Extract data for plotting
    years = [data['year'] for data in years_data]
    movie_counts = [data['count'] for data in years_data]
    time_taken = [data['time_taken'] for data in years_data]

    # Plot the data
    fig, ax1 = plt.subplots()

    # Plot movie count on the left y-axis
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Movie Count', color='tab:blue')
    ax1.plot(years, movie_counts, color='tab:blue', marker='o', label='Movie Count')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Create a second y-axis for time taken
    ax2 = ax1.twinx()
    ax2.set_ylabel('Time Taken (seconds)', color='tab:red')
    ax2.plot(years, time_taken, color='tab:red', marker='o', label='Time Taken')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # Title and show plot
    plt.title('REST API Performance for each Year')
    plt.tight_layout()
     # Save the plot to the static folder
    plot_filename = 'static/rest_movies_performance.png'
    plt.savefig(plot_filename)
    plt.close()

    return plot_filename  # Return the path to the saved plot
        

#####################################################################################
# Purpose:
#   Generate and save a plot of movie counts and API request times over a range of years.
#
# Parameters:
#   num_year (int): The number of past years to include in the plot, ending in the current year.
#
# Process:
#   - Converts `num_year` to an integer and calculates a range of years ending with the current year.
#   - For each year in the range:
#       - Calls `fetch_all_movies` to retrieve movies released in that year.
#       - Counts the movies and tracks the time taken to fetch them.
#       - Appends each year's data (movie count and time taken) to `years_data`.
#   - Extracts the years, movie counts, and time taken from `years_data` for plotting.
#   - Creates a plot with:
#       - Movie counts on the left y-axis.
#       - Time taken (seconds) on the right y-axis.
#   - Saves the plot as 'rest_movies_performance.png' in the static folder.
#
# Returns:
#   str: The file path to the saved plot image.
#######################################################################################
def fetch_movies_by_year(year, max_pages=10):
    """
    Fetches a list of movies for a specific year using a general search term
    and paginates results.

    Args:
        year (str): The year to search for movies.
        max_pages (int): The maximum number of pages to fetch (optional).

    Returns:
        list: A list of movie dictionaries with movie details.
    """
    movie_items = []
    search_term = "movie"  # General search term
    for page in range(1, max_pages + 1):
        params = {
            's': search_term,
            'y': year,
            'apikey': OMDB_API_KEY,
            'page': page
        }
        response = requests.get(OMDB_API_URL, params=params)
        
        # Check if the response is valid and contains movies
        if response.status_code == 200:
            data = response.json()
            if data.get("Response") == "True":
                for movie_data in data.get("Search", []):
                    movie_item = {
                        "id": movie_data.get("imdbID", "N/A"),
                        "title": movie_data.get("Title", "N/A"),
                        "year": movie_data.get("Year", "N/A"),
                        "genre": movie_data.get("Genre", "N/A").split(", "),  # Convert genres to a list
                        "director": movie_data.get("Director", "N/A"),
                        "actors": movie_data.get("Actors", "N/A").split(", "),  # Split actors into a list
                        "plot": movie_data.get("Plot", "N/A"),
                        "language": movie_data.get("Language", "N/A"),
                        "country": movie_data.get("Country", "N/A"),
                        "awards": movie_data.get("Awards", "N/A"),
                        "ratings": [{"source": rating.get("Source"), "value": rating.get("Value")} 
                                    for rating in movie_data.get("Ratings", [])],
                        "poster": movie_data.get("Poster", "N/A")  # URL to movie poster image
                    }
                    
                    movie_items.append(movie_item)
            else:
                break  # Stop if no more movies are found
        else:
            break  # Stop if there's an error in the response

    #itemcount = len(movie_items)
    #return movie_items
    #return render_template('movies.html', movies=movie_items)
    movie_count = len(movie_items)
    return render_template('movies.html', movies=movie_items, movie_count=movie_count)
       #return render_template('test.html')
    

###########################################################################
# Purpose:
#   Fetch a predefined list of movies from the OMDb API and structure the data
#   for display on a webpage.
#
# Parameters:
#   None
#
# Process:
#   - Defines a list of movie titles to fetch.
#   - For each title in the list:
#       - Calls `fetch_movie_data` to retrieve detailed movie information from the OMDb API.
#       - Structures each movie's data into a dictionary, including key fields like
#         title, year, genre, director, actors, plot, language, country, awards,
#         ratings, and poster image.
#       - Appends the structured movie data to the `movie_items` list.
#   - Renders an HTML template ('movies.html') to display the list of movies.
#
# Returns:
#   str: The rendered HTML page displaying the list of fetched movies.
###########################################################################
def get_movies():
    """
    Get a list of movie items from the OMDb API.

    Returns:
        list: A list of movie items, each containing key movie data.
    """
    # Example movie titles to fetch
    movie_titles = ['Inception', 'The Dark Knight', 'Interstellar']
    
    movie_items = []

    for title in movie_titles:
        movie_data = fetch_movie_data(title)
        
        # Define the movie item structure
        movie_item = {
            "id": movie_data.get("imdbID", "N/A"),
            "title": movie_data.get("Title", "N/A"),
            "year": movie_data.get("Year", "N/A"),
            "genre": movie_data.get("Genre", "N/A").split(", "),  # Convert genres to a list
            "director": movie_data.get("Director", "N/A"),
            "actors": movie_data.get("Actors", "N/A").split(", "),  # Split actors into a list
            "plot": movie_data.get("Plot", "N/A"),
            "language": movie_data.get("Language", "N/A"),
            "country": movie_data.get("Country", "N/A"),
            "awards": movie_data.get("Awards", "N/A"),
            "ratings": [{"source": rating.get("Source"), "value": rating.get("Value")} 
                        for rating in movie_data.get("Ratings", [])],
            "poster": movie_data.get("Poster", "N/A")  # URL to movie poster image
        }
        
        movie_items.append(movie_item)
        #return render_template('movies.html', movies=movie_items)
    
    return render_template('movies.html', movies=movie_items)
#return jsonify(movie_items)





