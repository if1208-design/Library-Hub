let usernameInput = document.getElementById("username");
let passwordInput = document.getElementById("pass");

function login(event) {
    event.preventDefault();

    let enteredUsername = usernameInput.value.trim();
    let enteredPassword = passwordInput.value.trim();
    let selectedRole = document.querySelector('input[name="role"]:checked');

    if (!enteredUsername || !enteredPassword) {
        alert("Fill all fields");
        return;
    }

    if (!selectedRole) {
        alert("Please select User or Admin");
        return;
    }

    let savedUser = JSON.parse(localStorage.getItem("user"));

    if (!savedUser) {
        alert("No account found, please sign up first.");
        return;
    }

    if (
        enteredUsername === savedUser.username &&
        enteredPassword === savedUser.password &&
        selectedRole.value === savedUser.isAdmin
    ) {
        if (savedUser.isAdmin === "true") {
            window.location.href = "/admin-dashboard/";
        } else {
            window.location.href = "/cover/";
        }
    } else {
        alert("Invalid login data.");
    }
}

let form = document.getElementById("loginForm");
form.addEventListener("submit", login);
