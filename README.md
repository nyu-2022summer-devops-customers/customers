# Customers
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
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

| HTTP Method | URL | Description|Return
| :--- | :--- | :--- | :--- |
|`GET` | `/` | Get information about the customer service  | Json
| `GET` | `/customers/{customer_id}` | Get customer by Customer_ID | CustomerModel Object
| `GET` | `/customers` | Returns a list of all the Customers | CustomerModel Object
| `POST` | `/customers` | Creates a new Customer record in the database | CustomerModel Object
| `PUT` | `/customers/{customer_id}` | Updates/Modify a Customer record in the database | CustomerModel Object
| `DELETE` | `/customers/{customer_id}` | Delete the Customer with the given id number | 204 Status Code
|`GET` | `/customers/{customer_id}/addresses` | Returns a list of all Addresses of a Customer | Address Object
|`GET` | `/customers/{customer_id}/addresses/{address_id}` | Get an Address by address_id | Customer Object
|`POST` | `/customers/{customer_id}/addresses` | Creates a new Address record in the database | Address Object
|`PUT` | `/customers/{customer_id}/addresses/{address_id}` | Updates/Modify an Address record in the database | AddressModel Object
|`DELETE` | `/customers/{customer_id}` | Delete the Address with the given address_id number | 204 Status Code

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
