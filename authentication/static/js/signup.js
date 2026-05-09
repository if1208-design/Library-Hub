let form = document.getElementById("signupForm");

form.addEventListener("submit", function(e) {
    e.preventDefault();

    let username = document.getElementById("username").value.trim();
    let email = document.getElementById("mail").value.trim();
    let password = document.getElementById("pass").value.trim();
    let confirmPassword = document.getElementById("cpass").value.trim();
    let selectedRole = document.querySelector('input[name="role"]:checked');

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

    form.submit();
});