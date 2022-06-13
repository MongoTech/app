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
`cd app` <br />
`python3.9 -m venv venv` <br />
`source ./venv/bin/activate`

## Verfify python version
`
python --version <br />
Python 3.9.12
`

## Run docker-compose
`docker-compose up -d`

Main thing is monga and provisioning

## Install poetry
`pip install poetry`

## Install poetry dependencies
`cd backend\app\app` <br />
`poetry install`

## Run application
`python main.py`

## For api testing you need postpam

[Postman](https://www.postman.com/downloads/)

# Configure first request Get Token
[get token request](https://gitlab.com/mongodb.tech/app/-/raw/main/docs/Screenshot_2022-06-13_at_09.59.11.png)
[add tests to save token](https://gitlab.com/mongodb.tech/app/-/blob/main/docs/Screenshot_2022-06-13_at_09.59.11.png)

In enviroment you need to define HOST = http://localhost:8001/api/v1 and pickup username and password from .env file


