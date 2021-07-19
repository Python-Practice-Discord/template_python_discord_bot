#!/bin/sh

set -e

. /home/default/.cache/pypoetry/virtualenvs/project-template-y8366zdl-py3.9/bin/activate

if [ "$DEBUG" == "true" ]; then
  export PYTHONDEVMODE=1
  export PYTHONTRACEMALLOC=1
fi

eval "$(python src/project_template/utils/load_secrets.py)"
exec $@
