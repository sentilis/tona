#!/bin/bash

set -e
# : ${TONA_ENV:=${TONA_ENV:="production"}}

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

function showHelp(){
echo "
    [--help [-h]]
    

    [--api-develop [-d]]

    [--web-develop [-w]]
    [--web-export [-e]] -- Transpiling WebApp to js & html

    [--production [tona]] -- Mode production
"
}

case "$1" in
    --help | -h )
        showHelp
    ;;

    --production | tona )        
        exec python3 tona web
        ;;

    --api-develop | -d)
        exec python tona/main.py web -e .env.example
        ;;
    --web-develop | -w)
        cd web
        exec npm run dev
        ;;
    --web-export | -e)
        cd web; 
        npm run export
        cp -vr __sapper__/export/* ../tona/templates
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