from flask import Flask, jsonify, request , render_template

from graphql_schema import schema  # Import your Query class from graphql_schema.py
from ariadne import graphql_sync
from ariadne.asgi import GraphQL
#from ariadne.flask import GraphQLView
import time
import pandas as pd

# Initialize Flask app
app = Flask(__name__)


###########################################################################
# Purpose:
#   This is a GraphQL endpoint that accepts POST requests containing 
#   GraphQL queries. It processes the queries using the GraphQL schema and 
#   returns the results as a JSON response.
#
# Parameters:
#   None (the input comes from the request body as JSON data).
#
# Process:
#   - Extracts the JSON data from the incoming POST request.
#   - Passes the JSON data to the `graphql_sync` function, along with:
#       - The GraphQL schema to validate and resolve the query.
#       - The request context (`request`) to be passed to the resolvers.
#       - The `debug` flag to help with debugging during development.
#   - Based on the success of the GraphQL query execution, determines the 
#     appropriate HTTP status code (200 for success, 400 for failure).
#   - Returns the result of the GraphQL query execution as a JSON response 
#     with the corresponding HTTP status code.
#
# Returns:
#   tuple:
#     - JSON response: The result of the executed GraphQL query.
#     - int: HTTP status code (200 for success, 400 for failure).
###########################################################################
@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    print(data)
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


###########################################################################
# Purpose:
#   This is a GraphQL Playground endpoint that returns a simple HTML page 
#   allowing developers to interactively explore and test GraphQL queries.
#   It serves the GraphQL Playground UI on a GET request to the "/graphql" 
#   URL.
#
# Parameters:
#   None (the function responds to GET requests to the "/graphql" endpoint).
#
# Process:
#   - Responds with the HTML content of the GraphQL Playground UI, allowing 
#     users to interact with the GraphQL schema and make queries.
#   - Sets the response's content type to 'text/html' to indicate that the 
#     response is an HTML document.
#   
# Returns:
#   tuple:
#     - HTML content: The GraphQL Playground interface as an HTML string.
#     - int: HTTP status code (200 for successful response).
#     - dict: Response header indicating the content type is 'text/html'.
###########################################################################
@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200, {'Content-Type': 'text/html'}



###########################################################################
# Purpose:
#   This function handles the `/showmovies` route, which executes a 
#   GraphQL query to fetch a list of movies and renders the data in an HTML 
#   page. It uses the GraphQL query 'allMovies' to fetch a list of movies 
#   from the GraphQL schema and displays the results on a webpage.
#
# Parameters:
#   None (the function handles GET requests to the `/showmovies` route).
#
# Process:
#   - Constructs a GraphQL query to fetch movie data from the server.
#   - Executes the GraphQL query using `graphql_sync` to fetch the movie data.
#   - If the query is successful:
#       - Extracts the movie data from the query result.
#       - Converts the movie data into a pandas DataFrame for easier handling.
#       - Renders the `movies.html` template with the fetched movie data.
#   - If the query fails, returns an error message in JSON format with a 
#     400 status code.
#
# Returns:
#   - If successful: A rendered HTML page displaying the fetched movie data 
#     using the `movies.html` template.
#   - If the query fails: A JSON response with an error message and a 400 
#     status code.
###########################################################################
@app.route('/showmovies')
def showmovies():
    data = {
        'operationName': 'allMovies',
        'variables': {},
        'query': 'query allMovies { allMovies(num_years: 5) { \
            id title year genre director actors plot language country awards poster } }'
    }
    
    # Execute the GraphQL query to fetch data
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    
    # Check if the query was successful
    if success:
        # Convert the result to a pandas DataFrame for rendering in HTML
        movies_data = result['data']['allMovies']
        df = pd.DataFrame(movies_data)
        
        # Render the data in the store.html template
        return render_template("movies.html", movies=movies_data, header="true")
        #return jsonify({"error": "Failed to rendoring"}), 400
    
    # If the query fails, return an error message
    return jsonify({"error": "Failed to fetch movies"}), 400


PLAYGROUND_HTML = """
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/graphql-playground-react@latest/build/static/css/index.css" />
    <script src="https://cdn.jsdelivr.net/npm/graphql-playground-react@latest/build/static/js/middleware.js"></script>
  </head>
  <body>
    <div id="root"></div>
    <script>
      window.addEventListener('load', function (event) {
        GraphQLPlayground.init(document.getElementById('root'), { endpoint: '/graphql' });
      });
    </script>
  </body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True, port=5000)


#query = QueryType()

# Resolver for the `hello` field
#@query.field("hello")
#def resolve_hello(_, info):
#    return "Hello, world!"


# Create the schema
#schema = make_executable_schema(type_defs, query)

# Add GraphQL endpoint with Ariadne
app.add_url_rule(
    '/graphql',
    view_func=GraphQL.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enables the GraphiQL interface
    )
)


# Route to display movie data in tabular form, filtered by year
@app.route("/movies")
def movie_list():
    years = request.args.get('years', type=int)  # Get the year from the query parameters (e.g., /movies?year=1994)

    # If no year is specified, default to showing all movies
    query = f'{{ allMovies(year: {years}) {{ title year genre director actors plot language country awards poster ratings {{ source value }} }} }}' if year else '{ allMovies { title year genre director actors plot language country awards poster ratings { source value } } }'

    # Start time for performance tracking
    start_time = time.time()

    # Execute the GraphQL query
    result = schema.execute(query)

    # End time
    end_time = time.time()
    time_taken = round(end_time - start_time, 2)

    # Get the movie count from the result
    movie_count = len(result.data.get("allMovies", []))

    # Return the rendered HTML template
    return render_template(
        "movies.html",
        movies=result.data.get("allMovies", []),
        movie_count=movie_count,
        time_taken=time_taken,
        year=years if years else "All"
    )


if __name__ == '__main__':
    app.run(debug=True)
#@app.route('/plot_restperformance')(plot_performance_rest)




