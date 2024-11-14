#!/bin/bash

docker compose build
docker compose down
rm -rf ./oxidized/pid
docker compose up -d
