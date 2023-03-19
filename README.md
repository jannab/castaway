# CastAway

CastAway is a system that simplifies and streamlines the creation of movies,
as well as the management and assignment of actors to those movies.

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes.

### Prerequisites

- Docker Desktop

### Installing

Create a local .env file.

Without Docker:
Install Dependencies in a virtual environment:
```
pip install -r requirements.txt
```

Using Docker:
Build:

```
docker build -t <your_imagename> .
```

And run the container:

```
docker run --name castaway --env-file=.env -p 80:8080 <your_imagename>
```

## Running the tests

```
python test_app.py
```

## Error Handling

Errors are returned as JSON objects in the following format:
```
{
    "error": "error description"
}
```
The API will return the following error types:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 405: Method Not Allowed
- 409: Conflict
- 422: Not Processable
- 500: Internal Server Error

## Endpoints
CastApi can be found here: https://castaway.onrender.com

- [Endpoint documentation on Swagger](https://app.swaggerhub.com/apis-docs/jannab/castawayapi/1.0.0-oas3#/)

## Acknowledgments

- [README template by Billie Thompson](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
- [RuntimeError: A 'SQLAlchemy' instance has already been registered on this Flask app](https://stackoverflow.com/questions/75523569/runtimeerror-a-sqlalchemy-instance-has-already-been-registered-on-this-flask)
