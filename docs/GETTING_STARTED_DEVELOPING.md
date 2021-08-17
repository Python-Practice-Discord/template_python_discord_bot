# Getting started

You can work on this project using any OS, but macOS and Linux are easiest. To use Windows you will
need to be using WSL/WSL2 as many commands are not supported by the regular Windows CLI.

There is a Makefile in the root of this project. It contains most of the commands you will need.
These include

* `make interactive` which will drop you into a shell inside the projects' docker environment.
* `make check` which will run a set of formatting and static analysis tools.
* `make test` which will run all of our tests inside the projects' docker environment.

## Setting up Your Dev Env

This project uses Docker and Docker-compose. This allows us to set up local databases, fake APIs and
generally reflect the production environment.

This project uses Poetry to lock, install, and serve our python dependencies both locally and in
Docker.

There are two parts of your environment. A local python installation (managed by poetry), and an
environment run inside of Docker containers (orchestrated by docker-compose and the Makefile)

### Local Poetry

Run the following steps to get your local python env set up and enable pre-commit.

* `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`
* `poetry install`
* `poetry shell`
* `pre-commit install`

### Docker

Follow these steps to get docker setup on your machine and get into shell inside the docker
environment.

* [Install docker on your machine](https://docs.docker.com/get-docker/)
    * HINT: If on linux `curl -fsSL https://get.docker.com -o get-docker.sh; sudo sh get-docker.sh`
* If on linux: [Install docker-compose on your machine](https://docs.docker.com/compose/install/)
* Run `make initialize_pg`
* Run `make interactive`

You now have a local postgres database with fake data, and the production schemas linked to your
CLI.
