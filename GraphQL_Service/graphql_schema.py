from flask import Flask,render_template
from ariadne import gql, make_executable_schema, QueryType
from ariadne.asgi import GraphQL

from utils import fetch_all_movies, plot_movies_performance, fetch_movies_by_years  # Import your shared functions

# Define the GraphQL schema (type definitions)
type_defs = gql("""
    type Rating {
        source: String
        value: String
    }

    type Movie {
        id: String
        title: String
        year: String
        genre: [String]
        director: String
        actors: [String]
        plot: String
        language: String
        country: String
        awards: String
        ratings: [Rating]
        poster: String
    }

    type MovieFetchPerformance {
        movie_count: Int
        time_taken: String
    }

    type PlotPerformance {
        plot_url: String
    }

    type Query {
        allMovies(num_years: Int): [Movie]
        fetchPerformance(year: Int): MovieFetchPerformance
        performancePlot(numYear: Int): PlotPerformance
    }
""")

query = QueryType()

# Define resolvers (functions that return data for each field)
#returns: All the movies in the given number of years

@query.field("allMovies")
def resolve_all_movies(obj, info, num_years=None):
    # Fetch movies by year
    all_movies  = fetch_movies_by_years(num_years)
    return all_movies
    #return render_template("movies.html", movies=all_movies, movie_count=len(all_movies), time_taken="N/A")

#returns:   All movie for a specific year
@query.field("fetchPerformance")
def resolve_fetch_performance(obj, info, year):
    # Fetch movies and measure performance
    movies, time_taken = fetch_all_movies(year)
    return {
        "movie_count": len(movies),
        "time_taken": f"{time_taken:.2f} seconds"
    }

#return the performance graph for data fetched for number of years
@query.field("performancePlot")
def resolve_performance_plot(obj, info, numYear):
    # Generate the performance plot URL
    plot_filename = plot_movies_performance(numYear, service_call='graphql')
    return {"plot_url": f"/{plot_filename}"}



schema = make_executable_schema(type_defs, query)

# Create the executable schema
#schema = make_executable_schema(type_defs, {
#    "Query": {
#        "allMovies": resolve_all_movies,
#        "fetchPerformance": resolve_fetch_performance,
#        "performancePlot": resolve_performance_plot
#    }
#})


