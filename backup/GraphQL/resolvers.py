from flask_microservice.GraphQL_Service.utils import plot_movies_performance


def resolve_performance_plot(root, info, num_year):
    plot_filename = plot_movies_performance(num_year, service_call="graphql")
    return {"plotUrl": plot_filename}