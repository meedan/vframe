#!/bin/bash
xhost +local:docker  # X11 display

IMAGE=vframe:ubuntu-18.04
docker images $IMAGE
USER="root"
GITHUB_REPO='https://github.com/adamhrv/vframe_check_api'

# Jupyter notebook port
while getopts 'p:' flag; do
  case "${flag}" in
    p) port="${OPTARG}";;
    *) error "Unexpected option ${flag}" ;;
  esac
done

if [ ! -z "$port" ]; then
    echo "Port selected: $port"
else
    port="9090"
fi

docker_port="$port:$port"

# directory for local data
dir_project="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
dir_data="$DIR_PROJECT/data"


# --------------------------------------------------------

echo "
 __      ________ _____            __  __ ______ 
 \ \    / /  ____|  __ \     /\   |  \/  |  ____|
  \ \  / /| |__  | |__) |   /  \  | \  / | |__   
   \ \/ / |  __| |  _  /   / /\ \ | |\/| |  __|  
    \  /  | |    | | \ \  / ____ \| |  | | |____ 
     \/   |_|    |_|  \_\/_/    \_\_|  |_|______|

VFRAME: Check API 
Shared data directory: $dir_data
Github: $GITHUB_REPO
"

docker run -it --privileged \
    --hostname $(hostname|sed -e 's/ubuntu-//')-vframe \
    --volume /tmp/.X11-unix:/tmp/.X11-unix \
    --volume="$dir_data:/data" \
    -e DISPLAY=unix$DISPLAY \
    -p $docker_port \
    -e "USER_HTTP=1" \
    $IMAGE "$@"