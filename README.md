# Customers
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
Created for NYU Devops project, Summer 2022. Microservices built for handling customer data for an e-commerce site.

## API Routes Documentation for Customers

| HTTP Method | URL | Description | Return
| :--- | :--- | :--- | :--- |
|`GET` | `/` | Get information about the customer service  | Json
| `GET` | `/customers/{customer_id}` | Get customer by Customer_ID | CustomerModel Object
| `GET` | `/customers` | Returns a list of all the Customers | CustomerModel Object
| `POST` | `/customers` | Creates a new Customer record in the database | CustomerModel Object
| `PUT` | `/customers/{customer_id}` | Updates/Modify a Customer record in the database | CustomerModel Object
| `DELETE` | `/customers/{customer_id}` | Delete the Customer with the given id number | 204 Status Code
|`GET` | `/customers/{customer_id}` | Returns a list of all Addresses of a Customer | Address Object
|`GET` | `/customers/{customer_id}/addresses/{address_id}` | Get an Address by address_id | Customer Object
|`POST` | `/customers/{customer_id}/addresses` | Creates a new Address record in the database | Address Object
|`PUT` | `/customers/{customer_id}/addresses/{address_id}` | Updates/Modify an Address record in the database | AddressModel Object
|`DELETE` | `/customers/{customer_id}` | Delete the Address with the given address_id number | 204 Status Code
