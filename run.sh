#!/bin/sh

cd `dirname $0`
/usr/bin/env PYTHONPATH=.:wokkel twistd -y main.py "$@"
