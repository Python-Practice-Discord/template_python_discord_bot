# Overview

NEVER put any secrets into a file that is not explicitly ignore in the `.gitignore` file.

This project is already setup to take secrets from environment variables. These can be set in many
ways.

# Setting env vars

## Locally

To add secrets to your env vars locally simply create a `.env` file at the root of this project.
The `.env` file will not be added to the Git repo.

The `.env` file is the same syntax as the `local.env` file. If the `.env` file exists it is
automatically loaded into env vars when the docker container is started `make interactive`. This is
done be the following code

```
Dockerfile Line 37 ENTRYPOINT
entrypoint.sh line 12 eval load_secrets.py
src/project_template/utils/load_secrets.py returns the correct key value pares and they get loaded env vars
```
