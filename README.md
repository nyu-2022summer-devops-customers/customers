# Customers
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Build Status](https://github.com/nyu-2022summer-devops-customers/customers/actions/workflows/tdd.yml/badge.svg)](https://github.com/nyu-2022summer-devops-customers/customers/actions)
[![Build Status](https://github.com/nyu-2022summer-devops-customers/customers/actions/workflows/bdd.yml/badge.svg)](https://github.com/nyu-2022summer-devops-customers/customers/actions)
[![codecov](https://codecov.io/gh/nyu-2022summer-devops-customers/customers/branch/master/graph/badge.svg?token=J40BECK4ZX)](https://codecov.io/gh/nyu-2022summer-devops-customers/customers)
[![Open in Remote - Containers](https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/nyu-2022summer-devops-customers/customers)

Created for NYU Devops project, Summer 2022. Microservices built for handling customer data for an e-commerce site.

## Contents

The project contains the following:

```text
.devcontainer
   |-- Dockerfile
   |-- devcontainer.json
   |-- docker-compose.yml
   |-- scripts
   |   |-- install-tools.sh
.flaskenv
.gitattributes
.github
   |-- ISSUE_TEMPLATE
   |   |-- bug_report.md
   |   |-- story.md
   |-- workflows
   |   |-- ci.yml
.gitignore
.pylintrc
Dockerfile
LICENSE
Makefile
Procfile
README.md
deploy
   |-- dev
   |   |-- deployment.yaml
   |   |-- postgresql.yaml
   |   |-- service.yaml
   |-- prod
   |   |-- deployment.yaml
   |   |-- postgresql.yaml
   |   |-- service.yaml
dot-env-example
features
   |-- customers.feature
   |-- environment.py
   |-- steps
   |   |-- customers_steps.py
   |   |-- web_steps.py
requirements.txt
service
   |-- __init__.py
   |-- config.py
   |-- models.py
   |-- routes.py
   |-- static
   |   |-- css
   |   |   |-- blue_bootstrap.min.css
   |   |   |-- cerulean_bootstrap.min.css
   |   |   |-- darkly_bootstrap.min.css
   |   |   |-- flatly_bootstrap.min.css
   |   |   |-- slate_bootstrap.min.css
   |   |-- index.html
   |   |-- js
   |   |   |-- bootstrap.min.js
   |   |   |-- jquery-3.6.0.min.js
   |   |   |-- rest_api.js
   |-- utils
   |   |-- cli_commands.py
   |   |-- error_handlers.py
   |   |-- log_handlers.py
   |   |-- status.py
setup.cfg
tests
   |-- __init__.py
   |-- factories.py
   |-- test_models.py
   |-- test_routes.py
```
Created for NYU Devops project, Summer 2022. Microservices built for handling customer data for an e-commerce site.

## API Routes Documentation for Customers

| HTTP Method | URL | Description|Input|Return
| :--- | :--- | :--- | :--- | :--- |
|`GET` |`/apidocs/` | Get the documentation API | None| :--- |HTML
|`GET` | `/api` | Get information about the customer service  |None|Json
| `GET` | `/api/customers/{customer_id}` | Get customer by Customer_ID |'customer_id': string|CustomerModel Object
| `GET` | `/api/customers` | Returns a list of all the Customers |None|CustomerModel Object
| `POST` | `/api/customers` | Creates a new Customer record in the database |{'first_name': string, 'last_name': string, 'nickname': string, 'email': string, 'gender': 'FEMALE' or 'MALE' or'UNKNOWN', 'birthday': string, 'password': string, 'is_active': boolean}|CustomerModel Object
| `PUT` | `/api/customers/{customer_id}` | Updates/Modify a Customer record in the database |'customer_id': string, 'first_name': string, 'last_name': string, 'nickname': string, 'email': string, 'gender': 'FEMALE' or 'MALE' or'UNKNOWN', 'birthday': string, 'password': string|CustomerModel Object
| `DELETE` | `/api/customers/{customer_id}` | Delete the Customer with the given id number |'customer_id': string|204 Status Code
|`GET` | `/api/customers/{customer_id}/addresses` | Returns a list of all Addresses of a Customer |'customer_id': string, 'address_id': integer|Address Object
|`GET` | `/api/customers/{customer_id}/addresses/{address_id}` | Get an Address by address_id |'customer_id': string|Customer Object
|`POST` | `/api/customers/{customer_id}/addresses` | Creates a new Address record in the database |{'customer_id': string, 'address_id': integer, 'address': string}| Address Object
|`PUT` | `/api/customers/{customer_id}/addresses/{address_id}` | Updates/Modify an Address record in the database |'customer_id': string, 'address_id': integer, 'address': string|AddressModel Object
|`DELETE` | `/api/customers/{customer_id}` | Delete the Address with the given address_id number |'customer_id': string|204 Status Code
|`GET`|`/api/customers?birthday=<string:birthday>`|List customers by birthday|'birthday': string|200 Status Code|
|`GET`|`/api/customers?nickname=<string:email>`|List customers by email|'email': string|200 Status Code|
|`GET`|`/api/customers?firstname=<string:firstname>&lastname=<string:lastname>`|List customers by their name|'firstname': string, 'lastname': string|200 Status Code|
|`GET`|`/api/customers?nickname=<string:nickname>`|List customers by nickname|'nickname': string|200 Status Code|
|`PUT`|`/api/customers/<int:customer_id>/activate`|Active a customer|--|204 Status Code|
|`DELETE`|`/api/customers/<int:customer_id>/deactivate`|Deactive a customer|--|204 Status Code|

## Prerequisite Software Installation

This lab uses Docker and Visual Studio Code with the Remote Containers extension to provide a consistent repeatable disposable development environment for all of the labs in this course.

You will need the following software installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Visual Studio Code](https://code.visualstudio.com)
- [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension from the Visual Studio Marketplace

All of these can be installed manually by clicking on the links above or you can use a package manager like **Homebrew** on Mac of **Chocolatey** on Windows.

Alternately, you can use [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/) to create a consistent development environment in a virtual machine (VM). 

You can read more about creating these environments in my article: [Creating Reproducable Development Environments](https://johnrofrano.medium.com/creating-reproducible-development-environments-fac8d6471f35)

## Bring up the development environment

To bring up the development environment you should clone this repo, change into the repo directory:

```bash
$ git clone git@github.com:nyu-2022summer-devops-customers/customers.git
$ cd customers
```

Depending on which development environment you created, pick from the following:

### Start developing with Visual Studio Code and Docker

Open Visual Studio Code using the `code .` command. VS Code will prompt you to reopen in a container and you should say **yes**. This will take a while as it builds the Docker image and creates a container from it to develop in.

```bash
$ code .
```

Note that there is a period `.` after the `code` command. This tells Visual Studio Code to open the editor and load the current folder of files.

Once the environment is loaded you should be placed at a `bash` prompt in the `/app` folder inside of the development container. This folder is mounted to the current working directory of your repository on your computer. This means that any file you edit while inside of the `/app` folder in the container is actually being edited on your computer. You can then commit your changes to `git` from either inside or outside of the container.


## Running TDD tests

As developers we always want to run the tests before we change any code. That way we know if we broke the code or if someone before us did. Always run the test cases first!

Run the tests using `nosetests`

```shell
$ nosetests
```

Nose is configured via the included `setup.cfg` file to automatically include the flags `--with-spec --spec-color` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

Nose is also configured to automatically run the `coverage` tool and you should see a percentage-of-coverage report at the end of your tests. If you want to see what lines of code were not tested use:

```shell
$ coverage report -m
```

This is particularly useful because it reports the line numbers for the code that have not been covered so you know which lines you want to target with new test cases to get higher code coverage.

You can also manually run `nosetests` with `coverage` (but `setup.cfg` does this already)

```shell
$ nosetests --with-coverage --cover-package=service
```

Try and get as close to 100% coverage as you can.

It's also a good idea to make sure that your Python code follows the PEP8 standard. `flake8` has been included in the `requirements.txt` file so that you can check if your code is compliant like this:

```shell
$ flake8 --count --max-complexity=10 --statistics service
```

I've also included `pylint` in the requirements. Visual Studio Code is configured to use `pylint` while you are editing. This catches a lot of errors while you code that would normally be caught at runtime. It's a good idea to always code with pylint active.

## Running the service

The project uses *honcho* which gets it's commands from the `Procfile`. To start the service simply use:

```shell
$ make run
```

You should be able to reach the service at: http://localhost:8000. The port that is used is controlled by an environment variable defined in the `.flaskenv` file which Flask uses to load it's configuration from the environment by default.


## Running BDD tests

To run BDD tests, you should start the service first, then using `behave` command to do BDD tests.

To start the service:

```shell
$ make run
```

Then open another terminal to run BDD tests:

```shell
$ behave
```

## What's featured in the project?

    * app/routes.py -- the main Service routes using Python Flask
    * app/models.py -- the data model using SQLAlchemy
    * tests/test_routes.py -- test cases against the Customer service
    * tests/test_models.py -- test cases against the Customer model
  
## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
