# Messaging App

## System dependencies
Ensure you have the following installed:
* Python >= 3.12 ([python.org](https://www.python.org/))
* Docker ([docker.com](https://www.docker.com/))

## Setup

Clone this repo and navigate to project root
```bash
git clone git@github.com:vipoi/message-app.git
cd message-app
```

Create a new virtual environment
```bash
python -m venv venv
```

Activate the virtual environment for this shell
```bash
source venv/bin/activate
which python
# path/to/project/venv/bin/python
```

Install the requirements
```bash
# Install package dependencies
pip install -r requirements.txt
```

Start the database service using docker. 
```bash
docker compose up -d
```

## Running

#### Running migrations
First time, you'll need to migrate the database
```bash
python manage.py migrate
```

#### Running tests
```bash
python manage.py test
```

#### Starting the development server
```bash
python manage.py runserver
```

If everything went well, you should see a message similar to this one:
```
System check identified no issues (0 silenced).
November 07, 2024 - 11:23:47
Django version 5.1.3, using settings 'messageapp.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Api Usage

Visit [http://localhost:8000/docs](http://localhost:8000/openapi.json) to view the generated swagger documentation. You may also download the OpenAPI spec at [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json) and import it into postman, insomnia or other api tool with OpenApi support.

The api uses basic auth for authentication, 

## Curl Examples

#### Create a user account
```bash
curl -X POST "http://localhost:8000/accounts/" \
-H "Content-Type: application/json" \
-d '{
  "username": "user1",
  "password": "tekopp1234",
  "password_confirm": "tekopp1234"
}'
```

#### Get messages for your account
```bash
curl -u user1:tekopp1234 "http://localhost:8000/messages/"
```

#### Get messages to/from a specific user
```bash
curl -u user1:tekopp1234 "http://localhost:8000/messages/?username=user2"
```

#### Get messages to/from a specific user, using offset and limit
```bash
curl -u user1:tekopp1234 "http://localhost:8000/messages/?username=user2&offset=10&limit=100"
```

Send a message to another account
```bash
curl -u user1:tekopp1234 -X POST "http://localhost:8000/messages/" \
-H "Content-Type: application/json" \
-d '{
  "receiver": "user2",
  "content": "My message"
}'
```

## Extensions:
* Authorization model with object-level permissions
* Linting and style guide enforcements
* Simple client application
