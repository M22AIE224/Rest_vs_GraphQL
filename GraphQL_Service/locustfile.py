from locust import HttpUser, TaskSet, task, between

class GraphQLApiUser(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def query_all_movies(self):
        query = """
        query allMovies($num_years: Int) {
          allMovies(num_years: $num_years) {
            title
            year
            genre
            director
            actors
            plot
            language
            country
            awards
            poster
          }
        }
        """
        variables = {
            "num_years": 3
        }
        
        payload = {
            "query": query,
            "variables": variables
        }


        response = self.client.post("/graphql", json={"query": query})

        # Check the response status code and the content
        if response.status_code == 200:
            print("Response: ", response.json())
        else:
            print(f"Error: {response.status_code} - {response.text}")

 
