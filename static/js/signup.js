function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let form = document.getElementById("signupForm");

form.addEventListener("submit", async function(e) {
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

    try {
        // Send to Django backend
        const response = await fetch('/signup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: new URLSearchParams({
                'username': username,
                'email': email,
                'password': password,
                'Is_Admin': selectedRole.value
            })
        });

        if (response.redirected) {
            // Django redirects to login page on success
            alert("Account created successfully!");
            window.location.href = "/login/";
        } else {
            const text = await response.text();
            if (text.includes('already exists')) {
                alert("Username already exists!");
            } else {
                alert("Signup failed. Please try again.");
            }
        }
    } catch (error) {
        console.error('Signup error:', error);
        alert("Signup failed. Please try again.");
    }
});