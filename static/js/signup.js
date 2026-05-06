let form = document.getElementById("signupForm");

form.addEventListener("submit", function(e) {
    e.preventDefault();

    let username = document.getElementById("username").value.trim();
    let email = document.getElementById("mail").value.trim();
    let password = document.getElementById("pass").value.trim();
    let confirmPassword = document.getElementById("cpass").value.trim();
    let selectedRole = document.querySelector('input[name="Is_Admin"]:checked');

    if (!username || !email || !password || !confirmPassword) {
        alert("Please fill all fields");
        return;
    }

    if (!selectedRole) {
        alert("Please select User or Admin");
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    let userData = {
        username: username,
        email: email,
        password: password,
        isAdmin: selectedRole.value
    };

    localStorage.setItem("user", JSON.stringify(userData));
    alert("Account created successfully!");
    window.location.href = "/login/";
});
