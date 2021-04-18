#!/bin/bash
set -ex

if [ "$(uname)" == "Darwin" ];then
    echo "can only run on Debian9, but not MacOS"
    exit 1
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ];then
    echo "current os is Linux"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ];then
    echo "can only run on Debian9, but not Windows"
    exit 1
fi
