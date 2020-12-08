#!/bin/sh -e

set -a # Cause all environment variables to be automatically exported

# Source all environment files, sorted in alphabetical order
source_env() {
    for env_file in /openedx/env/$1/*.env
    do
        . $env_file
    done
}

# First, source production env
source_env production
if [ "$NODE_ENV" = "development" ]
then
    # Development settings override production settings
    source_env development
fi

set +a

exec "$@"