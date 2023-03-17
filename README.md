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
pip install -r requirememnts.txt
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
    "success": False,
    "error": 400,
    "message": "bad request"
}
```
The API will return the following error types:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 409: Conflict
- 422: Not Processable
- 500: Internal Server Error

## Endpoints

- [Endpoints on Swagger](https://app.swaggerhub.com/apis-docs/jannab/CastAway/1.0.0#/)

## Acknowledgments

- [README template by Billie Thompson](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
- [RuntimeError: A 'SQLAlchemy' instance has already been registered on this Flask app](https://stackoverflow.com/questions/75523569/runtimeerror-a-sqlalchemy-instance-has-already-been-registered-on-this-flask)
