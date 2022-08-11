Feature: The customers service back-end
    As a Shop owner
    I need a RESTful catalog service
    So that I can keep track of all my customers accounts

Background:
    Given the server is started
    Given the following customers
        | first_name | last_name    | nickname | password | email         | gender  | birthday   | is_active |
        | Karayan    | Calarook     | K        | xxxx     | em123@nyu.edu | MALE    | 2021-07-30 | True      |
        | Zayne      | Wood         | Z        | xxxx     | em456@nyu.edu | FEMALE  | 1999-04-30 | True      |
        | Dominique  | Caligari     | D        | xxxx     | em789@nyu.edu | MALE    | 1941-07-22 | False     |
    Given the following addresses
        | address                                    |
        | 251 Mercer St, New York, NY 10012          |
        | 70 Washington Square S, New York, NY 10012 |
        | 60 5th Ave, New York, NY 10011             |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customers RESTful API Service" in the title
    And I should not see "404 Not Found"

Scenario: Create and Retrieve a Customer
    When I visit the "Home Page"
    And I set the "First Name" to "Gralrur"
    And I set the "Last Name" to "Lord Of Fire"
    And I set the "Nickname" to "Gral"
    And I set the "Password" to "xxxx"
    And I set the "Email" to "em730@nyu.edu"
    And I select "Male" in the "Gender" dropdown
    And I set the "Birthday" to "09-01-1939"
    And I select "True" in the "Is Active" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "First Name" field should be empty
    And the "Last Name" field should be empty
    And the "Nickname" field should be empty
    And the "Password" field should be empty
    And the "Email" field should be empty
    And the "Gender" field should be empty
    And the "Birthday" field should be empty
    And the "Is Active" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Gralrur" in the "First Name" field
    And I should see "Lord Of Fire" in the "Last Name" field
    And I should see "Gral" in the "Nickname" field
    And I should see "xxxx" in the "password" field
    And I should see "em730@nyu.edu" in the "Email" field
    And I should see "Male" in the "Gender" dropdown
    And I should see "1939-09-01" in the "Birthday" field
    And I should see "True" in the "Is Active" dropdown

Scenario: Update a Customer
    When I visit the "Home Page"
    And I set the "First Name" to "Karayan"
    And I press the "search" button
    Then I should see "Karayan" in the "First Name" field
    And I should see "Calarook" in the "Last Name" field
    And I should see "K" in the "Nickname" field
    And I should see "xxxx" in the "password" field
    And I should see "em123@nyu.edu" in the "email" field
    And I should see "Male" in the "Gender" dropdown
    And I should see "2021-07-30" in the "Birthday" field
    And I should see "True" in the "Is Active" dropdown
    When I change "Nickname" to "Kara"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Kara" in the "Nickname" field

Scenario: List all Customers
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Karayan" in the results
    And I should see "Zayne" in the results
    And I should see "Dominique" in the results

Scenario: Query customers by email
    When I visit the "Home Page"
    And I set the "email" to "em456@nyu.edu"
    And I press the "Search" button
    Then I should see "em456@nyu.edu" in the "email" field
    And I should see "Zayne" in the "First Name" field
    And I should see "Wood" in the "Last Name" field
    And I should see the message "Success"

Scenario: Query customers by nickname
    When I visit the "Home Page"
    And I set the "nickname" to "D"
    And I press the "Search" button
    Then I should see "D" in the "nickname" field
    And I should see "Dominique" in the "First Name" field
    And I should see "Caligari" in the "Last Name" field
    And I should see the message "Success"
    
Scenario: Delete a Customer
    When I visit the "Home Page"
    And I press the "Search" button
    And I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Customer has been Deleted!"


Scenario: Activate a Customer
    When I visit the "Home Page"
    And I press the "Search" button
    And I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Deactivate" button
    And I press the "Activate" button
    Then I should see the message "Customer activated"


Scenario: Deactivate a Customer
    When I visit the "Home Page"
    And I press the "Search" button
    And I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Deactivate" button
    Then I should see the message "Customer deactivated"


Scenario: List all Addresses of a Customer
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Karayan" in the results
    When I copy the "Id" field
    And I paste the "Id_2" field
    And I press the "Address-Search" button
    Then I should see the message "Success"
    And I should see "251 Mercer St, New York, NY 10012" in the address results
    And I should see "70 Washington Square S, New York, NY 10012" in the address results
    And I should see "60 5th Ave, New York, NY 10011" in the address results

Scenario: Clear the address form
     When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Karayan" in the results
    When I copy the "Id" field
    And I paste the "Id_2" field
    And I press the "Address-Search" button
    Then I should see the message "Success"
    When I press the "address-clear" button
    Then the "address_id" field should be empty
    Then the "address" field should be empty
    Then the "id_2" field should be empty
 
Scenario: Retrieve an Adresses by customer_id and address_id
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Karayan" in the results
    When I copy the "id" field
    And I paste the "id_2" field
    And I press the "Address-Search" button
    Then I should see the message "Success"
    And I should see "251 Mercer St, New York, NY 10012" in the address results
    And I should see "70 Washington Square S, New York, NY 10012" in the address results
    And I should see "60 5th Ave, New York, NY 10011" in the address results
    When I press the "address-retrieve" button
    Then I should see the message "Success"
    And I should see "251 Mercer St, New York, NY 10012" in the "address" field

Scenario: Create an Adresses 
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Karayan" in the results
    When I copy the "id" field
    And I paste the "id_2" field
    And I set the "address" to "607 pavonia ave"
    And I press the "address-create" button
    Then I should see the message "Success"
    When I press the "Address-Search" button
    Then I should see the message "Success"
    And I should see "251 Mercer St, New York, NY 10012" in the address results
    And I should see "70 Washington Square S, New York, NY 10012" in the address results
    And I should see "60 5th Ave, New York, NY 10011" in the address results
    And I should see "607 pavonia ave" in the address results

Scenario: Update an Address
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Karayan" in the results
    When I copy the "id" field
    And I paste the "id_2" field
    And I press the "Address-Search" button
    Then I should see the message "Success"
    And I should see "251 Mercer St, New York, NY 10012" in the "address" field
    When I change "address" to "new address"
    And I press the "address-update" button
    Then I should see the message "Success"
    When I press the "address-search" button
    Then I should see "new address" in the address results

Scenario: Delete an Address
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Karayan" in the results
    When I copy the "id" field
    And I paste the "id_2" field
    And I press the "Address-Search" button
    Then I should see the message "Success"
    When I press the "Address-Delete" button
    Then I should see the message "Success"