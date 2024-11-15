import graphene
from graphene import ObjectType, String, List, Int
from flask_microservice.GraphQL_Service.utils import fetch_all_movies, plot_movies_performance  # Import the shared function

class RatingType(ObjectType):
    source = String()
    value = String()

class MovieType(ObjectType):
    id = String()
    title = String()
    year = String()
    genre = List(String)
    director = String()
    actors = List(String)
    plot = String()
    language = String()
    country = String()
    awards = String()
    ratings = List(RatingType)
    poster = String()

class MovieFetchPerformanceType(ObjectType):
    movie_count = Int()
    time_taken = String()

class PlotPerformance(ObjectType):
    plot_url = graphene.String()

class Query(ObjectType):
    all_movies = List(MovieType, year=Int())
    fetch_performance = graphene.Field(MovieFetchPerformanceType, year=Int())  # Define the year argument here

    # Add the new query for fetching performance plot
    performance_plot = graphene.Field(PlotPerformance, num_year=graphene.Int())

    def resolve_performance_plot(self, info, num_year):
        plot_filename = plot_movies_performance(num_year, service_call='graphql')
        return PlotPerformance(plot_url=f"/{plot_filename}")
    

    def resolve_all_movies(self, info, year):
        movies, _ = fetch_all_movies(year)
        return movies

    def resolve_fetch_performance(self, info, year):
        movies, time_taken = fetch_all_movies(year)
        return MovieFetchPerformanceType(
            movie_count=len(movies),
            time_taken=f"{time_taken:.2f} seconds"
        )
