let form = document.getElementById("loginForm");

form.addEventListener("submit", function (event) {

    let username = document.getElementById("username").value.trim();
    let password = document.getElementById("pass").value.trim();
    let selectedRole = document.querySelector('input[name="role"]:checked');

    if (!username || !password) {
        event.preventDefault();
        alert("Fill all fields");
        return;
    }

    if (!selectedRole) {
        event.preventDefault();
        alert("Please select User or Admin");
        return;
    }

});