from locust import HttpUser, TaskSet, task, between

class RestApiUser(HttpUser):
    host = "http://localhost:5000" 

    wait_time = between(1, 5)  # Simulates time between tasks (1 to 5 seconds)


    @task(1)
    def get_all_movies(self):
        self.client.get("/movies/2023")  # Replace with a year parameter

    @task(1)
    def get_movie_by_years(self):
        self.client.get("/moviesforyears/1") 


# python3 -m locust --host=http://127.0.0.1:5000