# Messaging App

## System dependencies
* Python 3.12.3 and Pip
* Docker

## Setup

Create a virtual environment
```bash
$ python -m venv venv
```

Activate the virtual environment for this shell
```bash
$ source venv/bin/activate
```

Install the requirements
```bash
# verify you're using the correct virtual environment
$ which python # => path/to/project/venv/bin/python
# Install package dependencies
$ pip install -r requirements.txt
```

## Running

Start the external dependencies using docker compose. The first time this is run, docker will fetch the container
images for postgresql and adminer. 
```bash
docker compose up
```


