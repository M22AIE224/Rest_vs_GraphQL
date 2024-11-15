# sde-project
GraphQL vs REST framework

# system Requirements 

Python 3.8

#Libraries
Flask
SQL-Alchamey
Ariadne
Pandas



# how to run GraphQL Endpoint

1. Go to GraphQL-app folder
2. Install all dependencies 
3. Run flask shell ( or initiate GraphQL endpoint as 'python app.py')
4. To query the application open the url http://127.0.0.1/graphql to run any graphic based query
5. Put the query and click on Run in the browser
6. Use the query with different parameters on same endpoint


# how to run load test
1. Open shell
3. Run pip install locust
4. Go to GraphQL-app folder
5. Run locust 'python3 -m locust --host=http://localhost:5000'
6. Open the url http://127.0.0.1:8089 in the browser
7. Define the Users and variations and run the test


# how to run REST Endpoint

1. Go to REST-app folder
2. Install all dependencies 
3. Run flask shell ( or initiate GraphQL endpoint as 'python app.py')
4. To query the application open the url http://127.0.0.1/ to run any REST enpoint call
5. Run all enpoints in different sessions in parallel


# how to run load test
1. Open shell
3. Run pip install locust
4. Go to REST-app folder
5. Run locust 'python3 -m locust --host=http://localhost:5000'
6. Open the url http://127.0.0.1:8089 in the browser
7. Define the Users and variations and run the test