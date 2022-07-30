$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.customer_id);
        $("#first_name").val(res.first_name);
        $("#last_name").val(res.last_name);
        $("#nickname").val(res.nickname);
        $("#email").val(res.email);
        $("#gender").val(res.gender);
        $("#birthday").val(res.birthday);
        if (res.is_active == true) {
            $("#is_active").val("true");
        } else {
            $("#is_active").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#customer_id").val("");
        $("#first_name").val("");
        $("#last_name").val("");
        $("#nickname").val("");
        $("#email").val("");
        $("#gender").val("");
        $("#birthday").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Customer
    // ****************************************

    $("#create-btn").click(function () {

        let first_name = $("#first_name").val();
        let last_name = $("#last_name").val();
        let nickname = $("#nickname").val();
        let email = $("#email").val();
        let gender = $("#gender").val();
        let birthday = $("#birthday").val();
        let is_active = $("#is_active").val() == "true";

        let data = {
            "first_name": first_name,
            "last_name": last_name,
            "nickname": nickname,
            "email": email,
            "gender": gender,
            "birthday": birthday,
            "is_active": is_active
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Customer
    // ****************************************

    $("#update-btn").click(function () {

        let customer_id = $("#customer_id").val();
        let first_name = $("#first_name").val();
        let last_name = $("#last_name").val();
        let nickname = $("#nickname").val();
        let email = $("#email").val();
        let is_active = $("#is_active").val() == "true";
        let gender = $("#pet_gender").val();
        let birthday = $("#pet_birthday").val();

        let data = {
            "first_name": first_name,
            "last_name": last_name,
            "nickname": nickname,
            "email": email,
            "gender": gender,
            "birthday": birthday,
            "is_active": is_active
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/customers/${customer_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Customer
    // ****************************************

    $("#retrieve-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/customers/${customer_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Customer
    // ****************************************

    $("#delete-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/customers/${customer_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Pet has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#customer_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#search-btn").click(function () {

        let first_name = $("#first_name").val();
        let last_name = $("#last_name").val();
        let nickname = $("#nickname").val();
        let birthday = $("#birthday").val();
        let email = $("#email").val();

        let queryString = ""

        if (first_name && last_name) {
            queryString += 'first name=' + first_name + 'last name=' + last_name
        }
        if (nickname) {
            queryString += 'nick name=' + nickname
        }
        if (email) {
            queryString += 'email=' + email
        }
        if (birthday) {
            if (queryString.length > 0) {
                queryString += '&birthday=' + birthday
            } else {
                queryString += 'birthday=' + birthday
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/customers?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">First Name</th>'
            table += '<th class="col-md-2">Last Name</th>'
            table += '<th class="col-md-2">Nickname</th>'
            table += '<th class="col-md-2">Gender</th>'
            table += '<th class="col-md-2">Email</th>'
            table += '<th class="col-md-2">Birthday</th>'
            table += '<th class="col-md-2">Active</th>'
            table += '</tr></thead><tbody>'
            let firstCustomer = "";
            for(let i = 0; i < res.length; i++) {
                let customer = res[i];
                table +=  `<tr id="row_${i}"><td>${customer.customer_id}</td><td>${customer.first_name}</td><td>${customer.last_name}</td><td>${customer.nickname}</td><td>${pet.gender}</td><td>${pet.email}</td><td>${pet.birthday}</td><td>${customer.is_active}</td></tr>`;
                if (i == 0) {
                    firstCustomer = customer;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstCustomer != "") {
                update_form_data(firstCustomer)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})