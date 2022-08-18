$(function () {

    const BASE_URL = '/api/customers'
    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.customer_id);
        $("#customer_first_name").val(res.first_name);
        $("#customer_last_name").val(res.last_name);
        $("#customer_nickname").val(res.nickname);
        $("#customer_password").val(res.password);
        $("#customer_email").val(res.email);
        $("#customer_gender").val(res.gender);
        $("#customer_birthday").val(res.birthday);
        if (res.is_active == true) {
            $("#customer_is_active").val("true");
        } else {
            $("#customer_is_active").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#customer_id").val("");
        $("#customer_first_name").val("");
        $("#customer_last_name").val("");
        $("#customer_nickname").val("");
        $("#customer_password").val("");
        $("#customer_email").val("");
        $("#customer_gender").val("");
        $("#customer_birthday").val("");
        $("#customer_is_active").val("");
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

        let first_name = $("#customer_first_name").val();
        let last_name = $("#customer_last_name").val();
        let nickname = $("#customer_nickname").val();
        let password = $("#customer_password").val();
        let email = $("#customer_email").val();
        let gender = $("#customer_gender").val();
        let birthday = $("#customer_birthday").val();
        let is_active = $("#customer_is_active").val() == "true";

        let data = {
            "first_name": first_name,
            "last_name": last_name,
            "nickname": nickname,
            "password": password,
            "email": email,
            "gender": gender,
            "birthday": birthday,
            "is_active": is_active
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: BASE_URL,
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

    $("#update-btn").click(function (){
        let customer_id = $("#customer_id").val();
        let first_name = $("#customer_first_name").val();
        let last_name = $("#customer_last_name").val();
        let nickname = $("#customer_nickname").val();
        let password = $("#customer_password").val();
        let email = $("#customer_email").val();
        let gender = $("#customer_gender").val();
        let birthday = $("#customer_birthday").val();
        let is_active = $("#customer_is_active").val() == "true";

        let data = {
            "first_name": first_name,
            "last_name": last_name,
            "nickname": nickname,
            "password": password,
            "email": email,
            "gender": gender,
            "birthday": birthday,
            "is_active": is_active
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `${BASE_URL}/${customer_id}`,
                contentType: "application/json",
                data: JSON.stringify(data),
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
            url: `${BASE_URL}/${customer_id}`,
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

         let customer_id = $("#customer_id").val()

         $("#flash_message").empty()

         let ajax = $.ajax({
             type: "DELETE",
             url: `${BASE_URL}/${customer_id}`,
             contentType: "application/json",
             data: '',
         })

         ajax.done(function(res){
             clear_form_data()
             flash_message("Customer has been Deleted!")
         });

         ajax.fail(function(res){
             flash_message("Server error!")
         });

     });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#search-btn").click(function () {

        let first_name = $("#customer_first_name").val();
        let last_name = $("#customer_last_name").val();
        let nickname = $("#customer_nickname").val();
        let birthday = $("#customer_birthday").val();
        let email = $("#customer_email").val();

        let queryString = ""

        if (first_name && last_name) {
            if (queryString.length > 0) {
                queryString += '&firstname=' + first_name
                queryString += '&lastname=' + last_name
            } else {
                queryString += 'firstname=' + first_name
                queryString += '&lastname=' + last_name
            }
        }
        if (nickname) {
            if (queryString.length > 0) {
                queryString += '&nickname=' + nickname
            } else {
                queryString += 'nickname=' + nickname
            }
         }
        if (email) {
            if (queryString.length > 0) {
                queryString += '&email=' + email
            } else {
                queryString += 'email=' + email
            }
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
            url: `${BASE_URL}?${queryString}`,
            contentType: "application/json",
            data: ''
        })
        

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-1">ID</th>'
            table += '<th class="col-md-2">First Name</th>'
            table += '<th class="col-md-2">Last Name</th>'
            table += '<th class="col-md-2">Nickname</th>'
            table += '<th class="col-md-3">Password</th>'
            table += '<th class="col-md-1">Gender</th>'
            table += '<th class="col-md-2">Email</th>'
            table += '<th class="col-md-2">Birthday</th>'
            table += '<th class="col-md-2">IS Active</th>'
            table += '</tr></thead><tbody>'
            let firstCustomer = "";
            for(let i = 0; i < res.length; i++) {
                let customer = res[i];
                table +=  `<tr id="row_${i}"><td>${customer.customer_id}</td><td>${customer.first_name}</td><td>${customer.last_name}</td><td>${customer.nickname}</td>
                    <td>${customer.password}</td><td>${customer.gender}</td><td>${customer.email}</td><td>${customer.birthday}</td><td>${customer.is_active}</td></tr>`;
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

    // ****************************************
    // Activate a Customer
    // ****************************************

    $('#activate-btn').click(function () {
        let customer_id = $("#customer_id").val();
    
        var ajax = $.ajax({
          type: 'PUT',
          url:`${BASE_URL}/${customer_id}/activate`,
          contentType: 'application/json',
          data: '',
        });
    
        ajax.done(function (res) {
          //alert(res.toSource())
          update_form_data(res);
          flash_message('Customer activated');
        });
    
        ajax.fail(function (res) {
          clear_form_data();
          flash_message(res.responseJSON.message);
        });
      });

    // ****************************************
    // Deactivate a Customer
    // ****************************************

    $('#deactivate-btn').click(function () {
        let customer_id = $("#customer_id").val();
    
        var ajax = $.ajax({
          type: 'DELETE',
          url:`${BASE_URL}/${customer_id}/deactivate`,
          contentType: 'application/json',
          data: '',
        });
    
        ajax.done(function (res) {
          //alert(res.toSource())
          update_form_data(res);
          flash_message('Customer deactivated');
        });
    
        ajax.fail(function (res) {
          clear_form_data();
          flash_message(res.responseJSON.message);
        });
      });
    
    // ****************************************
    //  F U N C T I O N S   F O R   A D D R E S S E S
    // ****************************************
    // Update the form with data from the response
    async function update_address_form(res,customer_id) {
        let item = res
        if (Array.isArray(res)) {
            item = res[0]
        }
        $("#customer_id_2").val(item.customer_id);
        $("#customer_address_id").val(item.address_id);
        $("#customer_address").val(item.address);
        flash_message("Success")
    }
    
    function reload_search_result(customer_id){
        let ajax = $.ajax({
            type: "GET",
            url: `${BASE_URL}/${customer_id}/addresses`,
            contentType: "application/json",
            data: ''
        })
        ajax.done(function(res){
            $("#address_search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Address ID</th>'
            table += '<th class="col-md-8">Address</th>'
            table += '</tr></thead><tbody>'
            let firstAddress = "";
            for(let i = 0; i < res.length; i++) {
                let address = res[i];
                table +=  `<tr id="row_${i}"><td>${address.customer_id}</td><td>${address.address_id}</td><td>${address.address}</td></tr>`;
                if (i == 0) {
                    firstAddress = address;
                }
            }
            table += '</tbody></table>';
            $("#address_search_results").append(table);
        });
    }
    
    function clear_address_form() {
        $("#customer_id_2").val("");
        $("#customer_address_id").val("");
        $("#customer_address").val("");
    }
    // ****************************************
    // Search for Customer Addresses by customer_id
    // ****************************************
    $("#address-search-btn").click(function () {

        let customer_id = $("#customer_id_2").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `${BASE_URL}/${customer_id}/addresses`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            $("#address_search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Address ID</th>'
            table += '<th class="col-md-8">Address</th>'
            table += '</tr></thead><tbody>'
            let firstAddress = "";
            for(let i = 0; i < res.length; i++) {
                let address = res[i];
                table +=  `<tr id="row_${i}"><td>${address.customer_id}</td><td>${address.address_id}</td><td>${address.address}</td></tr>`;
                if (i == 0) {
                    firstAddress = address;
                }
            }
            table += '</tbody></table>';
            $("#address_search_results").append(table);

            update_address_form(res).then(flash_message("Success"))
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Retrieve a Customer Address by customer_id and address_id
    // ****************************************
    $("#address-retrieve-btn").click(function () {
        let customer_id = $("#customer_id_2").val();
        let address_id=$("#customer_address_id").val();

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "GET",
            url: `${BASE_URL}/${customer_id}/addresses/${address_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            $("#customer_address").val(res.address);
            flash_message("Success");
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Customer Address by customer_id and address_id
    // ****************************************
    $("#address-delete-btn").click(function () {
        let customer_id = $("#customer_id_2").val();
        let address_id=$("#customer_address_id").val();

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "DELETE",
            url: `${BASE_URL}/${customer_id}/addresses/${address_id}`,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function(res){
            clear_form_data();
            // reload_search_result(customer_id);
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Create an Address
    // ****************************************
    $("#address-create-btn").click(function () {
        let customer_id = $("#customer_id_2").val();
        let address=$("#customer_address").val();

        var data={
            "customer_id":customer_id,
            "address":address,
        }

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: `${BASE_URL}/${customer_id}/addresses`,
            contentType: "application/json",
            data: JSON.stringify(data),
        })
        
        ajax.done(function(res){
            update_address_form(res).then(flash_message("Success"))
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Clear the address form
    // ****************************************
    $("#address-clear-btn").click(function () {
        $("#flash_message").empty();
        clear_address_form()
    });

    // ****************************************
    // Update a Customer Address
    // ****************************************
    $("#address-update-btn").click(function () {
        let customer_id = $("#customer_id_2").val();
        let address=$("#customer_address").val();
        let address_id=$("#customer_address_id").val();

        var data = {
            //"customer_id": customer_id,
            "customer_id": customer_id,
            "address": address,
            "address_id":address_id
        };

        var ajax = $.ajax({
                type: "PUT",
                url: `${BASE_URL}/${customer_id}/addresses/${address_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
        })

        ajax.done(function(res){
            update_address_form(res).then(flash_message("Success"))
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });

    });
})
