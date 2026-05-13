
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

let form = document.getElementById("loginForm");

form.addEventListener("submit", async function(e) {
    e.preventDefault();

    let username = document.getElementById("username").value.trim();
    let password = document.getElementById("pass").value.trim();
    let selectedRole = document.querySelector('input[name="role"]:checked');

    if (!username || !password) {
        alert("Fill all fields");
        return;
    }

    if (!selectedRole) {
        alert("Please select User or Admin");
        return;
    }

    try {
        const response = await fetch('/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: new URLSearchParams({
                'username': username,
                'password': password,
                'role': selectedRole.value
            })
        });

        if (response.redirected) {
            // Django redirects to admin-dashboard or cover on success
            window.location.href = response.url;
        } else {
            alert("Invalid username or password");
        }
    } catch (error) {
        console.error('Login error:', error);
        alert("Login failed. Please try again.");
    }
});