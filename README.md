# app.monogdb.tech

## Before you start you needd

* [Docker+Docker Compose](https://www.docker.com/ + https://docs.docker.com/compose/install/).
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Python 3.9](https://www.python.org/downloads/release/python-3913/)

Later you will need:
* [NodeJS 16+npm](https://nodejs.org/en/)

## Add ssh-keys for you profile
You need add keys [here](https://gitlab.com/-/profile/keys) [instruction how to generate](https://coderlessons.com/tutorials/devops/vyuchit-gitlab/gitlab-nastroika-kliucha-ssh)

## Git clone 
`git clone git@gitlab.com:mongodb.tech/app.git`

## Install venv
`cd app
python3.9 -m venv venv
source ./venv/bin/activate 
`

## Verfify python version
`
python --version
Python 3.9.12
`

## Run docker-compose
`docker-compose up -d`

Main thing is monga and provisioning

## Install poetry
`pip install poetry`

## Install poetry dependencies
`cd backend\app\app
poetry install`

## Run application
`python main.py`
