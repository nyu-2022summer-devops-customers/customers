# Customers
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
![Build Status](https://github.com/nyu-2022summer-devops-customers/customers/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/nyu-2022summer-devops-customers/customers/branch/master/graph/badge.svg?token=J40BECK4ZX)](https://codecov.io/gh/nyu-2022summer-devops-customers/customers)

Created for NYU Devops project, Summer 2022. Microservices built for handling customer data for an e-commerce site.

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters
service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── utils                  - utility package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants
tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```
Created for NYU Devops project, Summer 2022. Microservices built for handling customer data for an e-commerce site.

## API Routes Documentation for Customers

| HTTP Method | URL | Description|Input|Return
| :--- | :--- | :--- | :--- | :--- |
|`GET` | `/` | Get information about the customer service  |None|Json
| `GET` | `/customers/{customer_id}` | Get customer by Customer_ID |'customer_id': string|CustomerModel Object
| `GET` | `/customers` | Returns a list of all the Customers |None|CustomerModel Object
| `POST` | `/customers` | Creates a new Customer record in the database |{'first_name': string, 'last_name': string, 'nickname': string, 'email': string, 'gender': 'FEMALE' or 'MALE' or'UNKNOWN', 'birthday': string, 'password': string, 'is_active': boolean}|CustomerModel Object
| `PUT` | `/customers/{customer_id}` | Updates/Modify a Customer record in the database |'customer_id': string, 'first_name': string, 'last_name': string, 'nickname': string, 'email': string, 'gender': 'FEMALE' or 'MALE' or'UNKNOWN', 'birthday': string, 'password': string|CustomerModel Object
| `DELETE` | `/customers/{customer_id}` | Delete the Customer with the given id number |'customer_id': string|204 Status Code
|`GET` | `/customers/{customer_id}/addresses` | Returns a list of all Addresses of a Customer |'customer_id': string, 'address_id': integer|Address Object
|`GET` | `/customers/{customer_id}/addresses/{address_id}` | Get an Address by address_id |'customer_id': string|Customer Object
|`POST` | `/customers/{customer_id}/addresses` | Creates a new Address record in the database |{'customer_id': string, 'address_id': integer, 'address': string}| Address Object
|`PUT` | `/customers/{customer_id}/addresses/{address_id}` | Updates/Modify an Address record in the database |'customer_id': string, 'address_id': integer, 'address': string|AddressModel Object
|`DELETE` | `/customers/{customer_id}` | Delete the Address with the given address_id number |'customer_id': string|204 Status Code

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

### Using Vagrant and VirtualBox

Bring up the virtual machine using Vagrant.

```shell
$ vagrant up
$ vagrant ssh
$ cd /vagrant
```

This will place you in the virtual machine in the `/vagrant` folder which has been shared with your computer so that your source files can be edited outside of the VM and run inside of the VM.

## Running the tests

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
$ honcho start
```

You should be able to reach the service at: http://localhost:8000. The port that is used is controlled by an environment variable defined in the `.flaskenv` file which Flask uses to load it's configuration from the environment by default.

## Shutdown development environment

If you are using Visual Studio Code with Docker, simply existing Visual Studio Code will stop the docker containers. They will start up again the next time you need to develop as long as you don't manually delete them.

If you are using Vagrant and VirtualBox, when you are done, you can exit and shut down the vm with:

```shell
$ exit
$ vagrant halt
```

If the VM is no longer needed you can remove it with:

```shell
$ vagrant destroy
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
