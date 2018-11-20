$(() => {
    const page = window.location.href.split("/")[3];
    if (page === "") initHome();
    else if (page === "login") initLogin();
    else if (page === "register") initRegister();
    else if (page === "profile") initProfile();
    else if (page === "discover") initDiscover();
});

function initHome() {
    // Home js.
    console.log("Home");
}

function initLogin() {
    // Login js.
    console.log("Login");
    $('#loginButton').click(() => {
        let form = getFormData($("#login"));
        form.csrfmiddlewaretoken = getCookie("csrftoken");

        // Validate frontend here.
        let valid = true;
        if (!valid) {
            console.log("Not valid");
            return;
        }

        const url = "http://127.0.0.1:8000/api/login/";
        $.ajax({
            url: url,
            type: "POST",
            data: form,
            dataType: "json",
            success: (data, status) => {
                if (status) {
                    if (data.success) {
                        const next = getUrlParameter("next");
                        if (next !== undefined) {
                            window.location.replace("http://127.0.0.1:8000" + next);
                        } else {
                            window.location.replace("http://127.0.0.1:8000/" + data.redirect);
                        }
                    } else {
                        console.log("bad login")
                    }
                } else {
                    console.log("Unable to POST");
                }
            }
        });

        console.log(form)
    });
}

function initRegister() {
    // Register js.
    console.log("Register");
    $('#registerButton').click(() => {
        let form = getFormData($("#register"));
        form.csrfmiddlewaretoken = getCookie("csrftoken");

        // Validate frontend here.
        let valid = true;
        if (!valid) {
            console.log("Not valid");
            return;
        }

        // Need a username, use the email.
        form.username = form.email;

        const url = "http://127.0.0.1:8000/api/register/";
        $.ajax({
            url: url,
            type: "POST",
            data: form,
            dataType: "json",
            success: (data, status) => {
                if (status) {
                    if (data.success) {
                        window.location.replace("http://127.0.0.1:8000/" + data.redirect);
                    } else {
                        validateForm(data.errors);
                    }
                } else {
                    console.log("Unable to POST");
                }
            }
        });

    });
}

function initProfile() {
    // Profile js.
    console.log("Profile");

}

function initDiscover() {
    // Discover js.
    console.log("Discover");
    const date = new Date();
    const csrf = getCookie("csrftoken");
    let profiles = [];

    // GET data.
    const url = "http://127.0.0.1:8000/api/profiles/";
    $.ajax({
        url: url,
        type: "GET",
        data: "json",
        success: (data, status) => {
            if (status) {

                console.log(data);
                var profile   = document.getElementById("profile-template").innerHTML;
                var template = Handlebars.compile(profile);
        
                document.getElementById("profile-block").innerHTML = template(data);

                $('.profile-card').click((e) => {
                    const id = e.currentTarget.id + "Modal"
                    $('#' + id).modal();
                });

                addAllFuncs();


            }
        }
    });

    // Click on profile to view the modal.
    $('.profile-card').click((e) => {
        const id = e.currentTarget.id + "Modal"
        $('#' + id).modal();
    });


    function addAllFuncs(){
        $('.heat-icon').click((e) => {
            e.stopImmediatePropagation();
            $(this).removeClass('.heat-icon');
            $(this).addClass('.heat-icon-active');
            addAllFuncs();
            addHeat(e);    
        });

        $('.heat-icon-active').click((e) => {
            e.stopImmediatePropagation();
            $(this).removeClass('.heat-icon-active');
            $(this).addClass('.heat-icon');
            addAllFuncs();
            removeHeat(e);    
        });
    }


    function addHeat(e){
        const id = $(e.currentTarget).closest('.profile-card').attr('id');
        console.log("Make profile", id, "hot.");
        let form = {};
        form.username = id;
        form.csrfmiddlewaretoken = getCookie("csrftoken");
        //Making hot cal call
        $.ajax({
            url: "http://127.0.0.1:8000/api/heat/",
            type: "POST",
            data: form,
            dataType: "json",
            success: (data, status) => {
                if (status) {
                    console.log("made hot")
                }
            }
        });    
    }

    function removeHeat(e){
        const id = $(e.currentTarget).closest('.profile-card').attr('id');
        console.log("Delete", id, "Heat.");
        let form = {};
        form.username = id;
        form.csrfmiddlewaretoken = getCookie("csrftoken");
        //Making hot cal call
        $.ajax({
            url: "http://127.0.0.1:8000/api/heat/",
            type: "DELETE",
            data: form,
            dataType: "json",
            success: (data, status) => {
                if (status) {
                    console.log("Delete heat")
                }
            }
        });    
    }


    // On init set the user's age from their DOB.
    $(".age").each(function () {
        let dob = $(this).text();
        try {
            let diff = (date - new Date(dob)) / 1000;
            diff /= (60 * 60 * 24);
            let age = Math.abs(Math.round(diff / 365.25));
            if (isNaN(parseFloat(age))) {
                $(this).text("?");
            } else {
                $(this).text(age);
            }
        } catch (e) {
        }
    });

    // On init set the user's location to '?' if not specified.
    $(".location").each(function () {
        let loc = $(this).text();
        if (loc === "Town/City") {
            $(this).text("?");
        }
    });

    // On init set the user's adjectives and remove if none.
    $(".adjectives").each(function () {
        let adjectives = $(this).text();
        adjectives = adjectives.split(",").map(function (item) {
            return item.trim();
        });
        if (adjectives.length <= 1 && adjectives[0] === "adjective") {
            $(this).text("mysterious");
        } else {
            $(this).text(adjectives[0]);
            for (let i = 1; i < adjectives.length && i < 3; i++) {
                $(this).after("<small class='text-uppercase font-weight-bold text-secondary'>" + adjectives[i] + "</small>")
            }
        }
    });
}


// Find cookie and return its value.
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(";");
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == " ") {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

// Find param and return its value.
function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
}

// Extract data from form.
function getFormData($form) {
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function (n, i) {
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

// Validate profile.
function validateForm(errors) {
    if (errors.first_name) {
        $('#firstname').addClass("is-invalid");
        $('#errorFirstname').text(errors.first_name);
        err = true;
    } else {
        $('#firstname').removeClass("is-invalid").addClass("is-valid");
    }
    if (errors.last_name) {
        $('#lastname').addClass("is-invalid");
        $('#errorLastname').text(errors.last_name);
        err = true;
    } else {
        $('#lastname').removeClass("is-invalid").addClass("is-valid");
    }
    if (errors.email) {
        $('#email').addClass("is-invalid");
        $('#errorEmail').text(errors.email);
        err = true;
    } else {
        $('#email').removeClass("is-invalid").addClass("is-valid");
    }
    if (errors.username) {
        $('#email').addClass("is-invalid");
        $('#errorEmail').text("Email address is already registered.");
        err = true;
    } else {
        $('#email').removeClass("is-invalid").addClass("is-valid");
    }
    if (errors.password1) {
        $('#password').addClass("is-invalid");
        $('#errorPassword').text(errors.password1);
        err = true;
    } else {
        $('#password').removeClass("is-invalid").addClass("is-valid");
    }
    if (errors.password2) {
        $('#password2').addClass("is-invalid");
        $('#errorPassword2').text(errors.password2);
        err = true;
    } else {
        $('#password2').removeClass("is-invalid").addClass("is-valid");
    }

    return err;
}