from flask import Flask, render_template, request
from controllers import get_movies,fetch_movies_by_year,fetch_all_movies, plot_movies_performance, fetch_movies_by_years
import os
import requests

#app = Flask(__name__)
app = Flask(__name__,)


app.config.from_object('config.Config')

##########################################################################
# Its a REST Routing function which can be called as http://localhost/movies/<year>
# the purpose of the function is to retrieve and display a list of movies 
# released in a specified year.

# Parameters:
# - year (str): The release year of the movies to fetch, passed as a URL parameter.

# Process:
# - Calls `fetch_all_movies` function with the `year` parameter to retrieve the list of movies.
# - Renders the 'movies.html' template with the fetched movies list.

# Returns:
# - A rendered HTML page displaying the list of movies for the specified year.
###########################################################################
@app.route('/movies/<year>', methods=['GET'])
def get_all_movies(year):
    #year = getattr
    movies_list, _ = fetch_all_movies(year) #(fetch_movies_by_year)
    return render_template('movies.html', movies=movies_list)


###########################################################################
# Its a REST Routing function which can be called as http://localhost/moviesforyears/<years>
# The purpose of the function is to retrieve and display a list of movies 
# released in last number of specified years.

# Parameters:
# - years (str): A number of years for which movies to be extracted, passed as a URL parameter.

# Process:
# - Calls `fetch_movies_by_years` function with the `years` parameter to retrieve the list of movies 
#   released in last number of specified years.
# - Renders the 'movies.html' template with the fetched movies list.

# Returns:
# - A rendered HTML page displaying the list of movies for the specified years.
###########################################################################
@app.route('/moviesforyears/<years>', methods=['GET'])
def get_movies_by_years(years):
    #year = getattr
    movies_list = fetch_movies_by_years(years) #(fetch_movies_by_year)
    return render_template('movies.html', movies=movies_list)


###########################################################################
# Its a REST Routing function which can be called as http://localhost/performancebyyears/<years>
# The purpose of the function is to generate and display a performance plot 
# for movies released over specified number of years.

# Parameters:
# - years (str): A number of years for which to fetch and analyze movie performance data, 
#   passed as a URL parameter.

# Process:
# - Calls `plot_movies_performance` function with the `years` parameter to generate a plot showing 
#   the performance of movies over the specified number of years.
# - Receives the file path of the generated plot.
# - Renders the 'performance.html' template with the plot file path as `plot_url`.

# Returns:
# - A rendered HTML page displaying the performance plot for the specified years.
###########################################################################
@app.route('/performancebyyears/<years>')
def movies_performance(years):
    #num_year = 5  # Define the number of years to fetch data for
    plot_filename = plot_movies_performance(years)  # Call the function and get the plot file path
    
    print(plot_filename)
    return render_template('performance.html', plot_url=plot_filename)






if __name__ == '__main__':
    app.run(debug=True)
