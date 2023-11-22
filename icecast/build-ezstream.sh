#!/bin/bash
#
cp ../*.py .
docker build -f Dockerfile-ezstream -t ezstream .
