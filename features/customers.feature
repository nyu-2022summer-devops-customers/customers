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

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customers RESTful API Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "First Name" to "Gralrur"
    And I set the "Last Name" to "Lord Of Fire"
    And I set the "Nickname" to "Gral"
    And I set the "Password" to "xxxx"
    And I set the "Email" to "email@nyu.edu"
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