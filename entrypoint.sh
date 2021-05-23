#!/bin/bash

set -e

: ${TONA_ENV:=${TONA_ENV:="production"}}
: ${TONA_TZ:=${TONA_TZ:='UTC'}}
: ${TONA_STORAGE:=${TONA_STORAGE:="/tona/storage"}}

ARGS=()

function add_arg(){
    ARGS+=("$1")
    ARGS+=("$2")
}

function clean_build(){
    dirs=('./build' './dist' './tona.egg-info')
    for dir in "${dirs[@]}"; do
        if [ -d "$dir" ]; then
            rm -r $dir
        fi
    done 
}

case "$1" in
    --prod | tona )
        add_arg "--time-zone" "$TONA_TZ"
        add_arg "--storage" "$TONA_STORAGE"
        export TONA_ENV=$TONA_ENV
        exec tona webapp "${ARGS[@]}"
        ;;
    --dev)
        export TONA_ENV=dev
        exec python3 main.py webapp -d --storage storage --time-zone $(cat /etc/timezone)
        ;;
    --install)
        python3 setup.py install
        ;;
    --upgrade)
        pip uninstall tona 
        clean_build
        python3 setup.py install
        ;;
    --uninstall)
        pip uninstall tona 
        clean_build
        ;;
    *)
        exec "$@"
        ;;
esac

exit 1