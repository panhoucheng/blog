#!/bin/bash

git pull origin master \
        && docker-compose build \
        && docker-compose restart
