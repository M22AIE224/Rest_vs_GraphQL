import time
import requests
import matplotlib.pyplot as plt


# Define the OMDb API key and base URL
OMDB_API_KEY = '2a9f78a3'
OMDB_API_URL = 'http://www.omdbapi.com'


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

def plot_movies_performance(num_year, service_call):
    years_data = []

   
    # Ensure num_year is an integer, e.g., num_year = 5 for last 5 years
    for year in range(2024 - num_year - 1, 2024):
        movie_items, time_taken = fetch_all_movies(year)
        movie_count = len(movie_items)
        fetch_performance = {
            "year": year,
            "count": movie_count,
            "time_taken": time_taken
        }
        years_data.append(fetch_performance)

    # Extract data for plotting
    years = [data['year'] for data in years_data]
    movie_counts = [data['count'] for data in years_data]
    time_taken = [data['time_taken'] for data in years_data]

    # Plot the data
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Movie Count', color='tab:blue')
    ax1.plot(years, movie_counts, color='tab:blue', marker='o', label='Movie Count')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Time Taken (seconds)', color='tab:red')
    ax2.plot(years, time_taken, color='tab:red', marker='o', label='Time Taken')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title(f'{service_call.capitalize()} API Performance for each Year')
    plt.tight_layout()

    # Determine filename based on service_call
    plot_filename = f'static/{service_call}_movies_performance.png'

    # Save the plot to the specified filename
    plt.savefig(plot_filename)
    plt.close()

    return plot_filename