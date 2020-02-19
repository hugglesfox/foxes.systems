#!/usr/bin/env bash

pipenv run python3 -m blog

cd public

git add *
git commit -m $(date +%s)
git push origin master
