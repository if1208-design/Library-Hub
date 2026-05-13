document.addEventListener("DOMContentLoaded", function () {
    // Triggers active data pulls from the SQLite database as soon as layout loads
    renderBooks();
});

function renderBooks() {
    const searchInput = document.getElementById("dashboardSearch");
    const query = searchInput ? searchInput.value : "";

    // Communicates asynchronously with the backend library app view layer instead of localStorage
    fetch(`/api/books/?search=${encodeURIComponent(query)}`)
        .then(response => {
            if (response.status === 403) {
                alert("Access denied. Admin validation rules unverified.");
                window.location.href = "/login/";
                return;
            }
            return response.json();
        })
        .then(data => {
            if (!data) return;
            const tableBody = document.getElementById("bookTableBody");
            tableBody.innerHTML = "";

            if (data.books.length === 0) {
                tableBody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 30px 0;">No match metrics matching current context records found.</td></tr>`;
                return;
            }

            // Loop database inventory response items directly into table layout row sets
            data.books.forEach(book => {
                const status = book.is_borrowed ? "Borrowed" : "Available";
                const statusClass = book.is_borrowed ? "tag-borrowed" : "tag-available";
                const row = document.createElement("tr");
                
                row.innerHTML = `
                    <td><strong>#${book.id}</strong></td>
                    <td>${book.title}</td>
                    <td>${book.author}</td>
                    <td>${book.category}</td>
                    <td><span class="status-tag ${statusClass}">${status}</span></td>
                    <td class="action-cell">
                        <button class="tbl-edit-btn" onclick="editBook('${book.id}')">Edit</button>
                        <button class="tbl-delete-btn" onclick="deleteBook('${book.id}')">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error communicating with active API view database:", error));
}

// Hook dynamic on-input typing queries directly into input search bar layout element
const searchInput = document.getElementById("dashboardSearch");
if (searchInput) {
    searchInput.addEventListener("input", renderBooks);
}

function deleteBook(id) {
    if (!confirm("Are you sure you want to permanently delete this book entry from Papyrus Hub?")) return;

    // Direct database removal request using an asynchronous POST transmission loop
    fetch(`/api/books/delete/${id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"), // Django explicit CSRF cross-site protection wrapper
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Screen reload forces database calculations of numerical context counters to process instantly
            window.location.reload(); 
        } else {
            alert("Error: " + (data.error || "Could not clear record."));
        }
    })
    .catch(error => console.error("Transmission error inside backend processing routing:", error));
}

// Links cleanly to your teammate's dynamic primary key format: edit-book/<int:pk>/
function editBook(id) {
    window.location.href = `/edit-book/${id}/`;
}

// Utility module wrapper extracting active cookie protection frameworks out of document layer
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