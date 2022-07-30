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