# Readme

## Background
### Project Motivation
This project is the final demonstration of the skills learned in the Udacity Full-Stack course, featuring the use of:

* Application based on Python 3 and Flask
* Multiple class inheritance for Python objects
* Entity modelling using Postgresql
* Creating a number of APIs
* Utilising SQLAlchemy ORM to abstract the application's interaction with the database
* Authentication and RBAC utilising Auth0 as the identity prvoider
* Creating unit tests for the application APIs
* Deploy the application to Heroku

### Project abstract
A casting agency wants to manage the actors on their books and their commitments to filming movies.

The casting assistant can view actors, movies, roles, role-types and commitments. They can also create/delete records for actors to attach or detach them from movies (commitments).

The casting director has the all available privileges.

#### Future planned updates
1. An actor can have multiple commitments to multiple films, but the commitment dates must not overlap
2. A movie can have multiple actors starring in it and it can define the maximum number of actors per role, per movie (this is represented by the number of instances of role types associated to a movie)
3. A front end for this

### Highlighted issues to be solved
The original file structure [here](https://github.com/leogovan/fs-nano-capstone) of:

```
|-- /backend
    |-- /database
    |-- /migrations
     -- app.py
     -- auth.py
     -- etc..
|-- /frontend
|-- Procfile
|-- manage.py
|-- requirements.txt
|-- runtime.txt
|-- setup.sh
```

meant I was unable to complete the database migrations steps i.e. I had to move all the items in ```/backend``` out to the same level as the heroku deployment files. Running the below commands in /backend

```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
heroku run python manage.py db upgrade --app [my-app-name]
```

caused a ```ModuleNotFoundError: No module named 'models'``` and as yet, I am unable to resolve.

## Interacting with the live application
While there is no front end, you are able to use the supplied postman collection to interact with the application API.

Note: on first submission for project review, the included authentication tokens for the two roles will be valid. However since these only have a lifetime of 24 hours, you may need to regenerate the tokens and replace the expired ones in the collection manually. Instructions for generating new tokens can be found below in the Unit Testing section.


### Live Location
The live app is deployed to Heroku and located at https://fs-capstone-submission.herokuapp.com/ however, you will need the postman collection / tokens to interact directly with this.

### Endpoints
```GET '/movies'```

- Fetches a collection of movies
- Request arguments: none
- Returns: an object containing a list of objects representing all the available movies and a count of the total results

```json
{
    "movies": [
        {
            "director": "Louis Leterrier",
            "genre": "Action",
            "movie_id": 1,
            "movie_name": "Transporter 8",
            "release_date": "Tue, 31 Dec 2024 00:00:00 GMT"
        },
        {
            "director": "Richard Curtis",
            "genre": "Horror",
            "movie_id": 2,
            "movie_name": "Love Actually - The Revenge",
            "release_date": "Sun, 15 Jun 2025 00:00:00 GMT"
        }
    ],
    "success": true,
    "total_movies": 2
}
```

```POST '/movies'```

- Sends a post request to create a new movie
- Request body:
```json
{
    "movie_name": "Class Test Movie 3",
    "genre": "Genre",
    "release_date": "2022-02-20",
    "director": "Me"
}
```
- Returns: an object with a success True response

```json
{
    "success": true
}
```

```DELETE '/movies/{id}'```

- Deletes a specified movie using its id
- Request arguments: id - integer
- Returns: an object with a success True response and the deleted movie id 

```json
{
    "success": true,
    "deleted_movie_id": 1
}
```

```PATCH '/movies/{id}'```

- Updates a specified movie using its id
- Request arguments: id - integer
- Returns: an object with a success True response and the updated movie id 

```json
{
    "success": true,
    "patched_movie_id": 1
}
```

```GET '/actors'```

- Fetches a collection of actors
- Request arguments: none
- Returns: an object containing a list of objects representing all the available actors and a count of the total results

```json
{
    "actors": [
        {
            "actor_id": 1,
            "actor_name": "Hugh Grant",
            "age": "61",
            "gender": "M",
            "image_link": "https://cdn.mos.cms.futurecdn.net/27YxZH8yY9pMztx4WqpAa9.jpg"
        },
        {
            "actor_id": 2,
            "actor_name": "Jason Statham",
            "age": "54",
            "gender": "M",
            "image_link": "https://www.onthisday.com/images/people/jason-statham-medium.jpg"
        }
    ],
    "success": true,
    "total_actors": 2
}
```

```POST '/actors'```

- Sends a post request to create a new actor
- Request body:
```json
{
    "actor_name": "Stanley Tucci",
    "phone": "555-5555",
    "age": "61",
    "gender": "M",
    "image_link": "https://media.newyorker.com/photos/617c5762d45c99c32e2e4319/master/pass/Rosner-Tucci.jpg"
}
```
- Returns: an object with a success True response

```json
{
    "success": true
}
```

```DELETE '/actors/{id}'```

- Deletes a specified actor using its id
- Request arguments: id - integer
- Returns: an object with a success True response and the deleted actor id 

```json
{
    "success": true,
    "deleted_actor_id": 1
}
```

```GET '/roles'```

- Fetches a collection of roles
- Request arguments: none
- Returns: an object containing a list of objects representing all the available roles and a count of the total results

```json
{
    "roles": [
        {
            "movie_id": 1,
            "number": 1,
            "role_id": 1,
            "role_type_id": 1
        },
        {
            "movie_id": 1,
            "number": 2,
            "role_id": 2,
            "role_type_id": 2
        }
    ],
    "success": true,
    "total_roles": 2
}
```

```POST '/roles'```

- Sends a post request to create a new role
- Request body:
```json
{
    "role_number": "300",
    "role_type_id": "5",
    "movie_id": "1"
}
```
- Returns: an object with a success True response

```json
{
    "success": true
}
```

```DELETE '/roles/{id}'```

- Deletes a specified role using its id
- Request arguments: id - integer
- Returns: an object with a success True response and the deleted role id 

```json
{
    "success": true,
    "deleted_role_id": 1
}
```

```GET '/commitments'```

- Fetches a collection of commitments
- Request arguments: none
- Returns: an object containing a list of objects representing all the available commitments and a count of the total results

```json
{
    "commitments": [
        {
            "actor_id": 1,
            "commitment_id": 1,
            "end_date": "Wed, 01 Jun 2022 00:00:00 GMT",
            "movie_id": 1,
            "role_type_id": 1,
            "start_date": "Sat, 01 Jan 2022 00:00:00 GMT"
        },
        {
            "actor_id": 2,
            "commitment_id": 2,
            "end_date": "Thu, 01 Jun 2023 00:00:00 GMT",
            "movie_id": 3,
            "role_type_id": 1,
            "start_date": "Sun, 01 Jan 2023 00:00:00 GMT"
        }
    ],
    "success": true,
    "total_sommitments": 2
}
```

```POST '/commitments'```

- Sends a post request to create a new commitment
- Request body:
```json
{
    "start_date": "2022-02-20",
    "end_date": "2022-02-20",
    "movie_id": "2",
    "actor_id": "3",
    "role_type_id": "2"
}
```
- Returns: an object with a success True response

```json
{
    "success": true
}
```

```DELETE '/commitments/{id}'```

- Deletes a specified commitment using its id
- Request arguments: id - integer
- Returns: an object with a success True response and the deleted commitment id 

```json
{
    "success": true,
    "deleted_commitment_id": 1
}
```

```GET '/role-types'```

- Fetches a collection of role-types
- Request arguments: none
- Returns: an object containing a list of objects representing all the available role-types and a count of the total results

```json
{
    "role_types": [
        {
            "role_type": "star",
            "role_types_id": 1
        },
        {
            "role_type": "co-star",
            "role_types_id": 2
        },
        {
            "role_type": "supporting",
            "role_types_id": 3
        },
        {
            "role_type": "featured_extra",
            "role_types_id": 4
        },
        {
            "role_type": "background",
            "role_types_id": 5
        }
    ],
    "success": true,
    "total_role_types": 5
}
```

## Running the app locally
### Python and Postgres
You will need Python3 installed. While this app was originally written with v3.9, it should work with 3.7 and beyond.

You will also need Postgres installed locally. This app was built using v13.2.

### Python Modules and Other Dependencies
Navigate to the root folder and create a virtual environment using virtualenv:

```bash
python3 -m venv venv
```

Activate the virtual environment using ```source venv/bin/activate``` and install the dependencies listed in the ```requirements.txt``` file:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Database Model
This is a ERD diagram of the database structure and the permissions available for the two roles:

![Casting Agency ERD](https://lucid.app/publicSegments/view/7a26424c-f3d3-4d5c-bd7b-c6a80e2d3521/image.jpeg)

### Create the Database
With Postgres running, create a new database:

```bash
createdb fs-capstone-submission
```

### Creating the Tables
The tables will be set up by launching the app for the first time - see below.

### Set the environment variables
Note: ensure the virtual environment is running.

```bash
chmod +x setup.sh
source setup.sh
```

### Launch the app

From the root directory in the terminal, ensure the virtual environment is activated and run the below:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

This will launch the app and set up the tables. At this point you can choose to run the sample data setup described below.

#### Optional Step: Sample Data Import
With Postgres running and the tables created, you can optionally inject some sample data into the database to get started by using the ```test-sample-data.psql``` file provided. From the main folder, in the terminal run:

```bash
psql fs-capstone-submission < database/test-sample-data.psql
```

## Unit Testing
In test_app.py, there are a set of unit tests that can be run to simulate interacting with the live API.

### Test prep
To run the unit tests you will need to first:

1. Generate tokens for both the director and assistant roles (without these, they will all fail authentication); and
2. Add these tokens to the ```.env``` file

Note: the ```.env``` file would not normally be included in a public repository but they have this time for the purposes of this project.

#### Generate the tokens and add to .env
1. Open an incognito browser
2. Navigate to https://fsnd-leogovan.eu.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=pZ3LmwWCftyO1H8zNgLENgQdGFGz8iUs&redirect_uri=http://localhost:5000
3. Login as the director (```casting-director@example.com / P@ssword123```)
4. Copy and paste the resulting url - it will look something like this:

```http://localhost:5000/#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJjNy1ISU5NSzVpQ2s0NG5EdEVNTSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbGVvZ292YW4uZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYyMmE2ZDY1ZjI0ZmI2MDA3MDYzNjg2YyIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNjQ3MjczNDQ4LCJleHAiOjE2NDczNTk4NDgsImF6cCI6InBaM0xtd1dDZnR5TzFIOHpOZ0xFTmdRZEdGR3o4aVVzIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOmNvbW1pdG1lbnRzIiwiZGVsZXRlOm1vdmllcyIsImRlbGV0ZTpyb2xlcyIsImdldDphY3RvcnMiLCJnZXQ6Y29tbWl0bWVudHMiLCJnZXQ6bW92aWVzIiwiZ2V0OnJvbGVzIiwiZ2V0OnJvbGUtdHlwZXMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6Y29tbWl0bWVudHMiLCJwb3N0Om1vdmllcyIsInBvc3Q6cm9sZXMiXX0.fxJfQty4kLz7xnA80C-qdUM-lfq3WgkpJXHgrSLjdVcaYKtFRkhYxsDa-89B6RLe3D1pk9jWT9rTzli_SnmZfHVD1BbglSAAeFwoFS9wRwv1ag5_KxgxVS2VDzovYagNgBJmt3saiJFhb1uR4_If2WZTuXCKbBn5Xz80rKdC4FL_XYAoQsGZOWEEc353DSnZcXpp0llIJK-IMZRbBr9Sd9cdnZaW4pEcyBHE8UoODSk21-VEtGgglFWCaQ8_T1_Ifr8FQGhKgEZahHiL4gs3VFCc2uyvnwE_2Bli4nfkceCpXBvaJPuap488LlvhijFz3ungxKbfJJNZ0E6tm_IsgQ&expires_in=86400&token_type=Bearer```

5. Copy the token (it's the long value inbetween ```http://localhost:5000/#access_token=``` and ```&expires_in=86400&token_type=Bearer```)
6. Paste it in ```.env``` as the value for ```CASTING_DIRECTOR_TOKEN=```
7. Repeat steps 1-5 for the assistant (```casting-assistant@example.com / P@ssword123```) and paste the value in ```.env``` for ```CASTING_ASSISTANT_TOKEN=```

### Run the tests
Ensure that the environment variables have been set as described above. Then, from the root folder (with Postgres running):

```bash
dropdb fs-capstone-submission_test
createdb fs-capstone-submission_test
psql fs-capstone-submission_test < database/test-sample-data.psql
python test_app.py
```