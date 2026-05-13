document.addEventListener("DOMContentLoaded", function () {
    // Initial fetch to load table rows from DB
    fetchBooks();

    // Attach dynamic input event listener to run live search filtering queries
    const searchInput = document.getElementById("dashboardSearch");
    if (searchInput) {
        searchInput.addEventListener("input", function () {
            fetchBooks(this.value);
        });
    }
});

// Fetch books from backend API with optional search query parameter
function fetchBooks(searchQuery = "") {
    let url = "/api/books/";
    if (searchQuery) {
        url += `?search=${encodeURIComponent(searchQuery)}`;
    }

    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error("Network response error");
            return response.json();
        })
        .then(data => {
            renderBooksTable(data.books);
        })
        .catch(error => console.error("Error fetching books data:", error));
}

// Dynamically populates the standard HTML table rows
function renderBooksTable(books) {
    const tableBody = document.getElementById("bookTableBody");
    tableBody.innerHTML = "";

    if (!books || books.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; padding: 20px;">No books matched your criteria</td></tr>`;
        return;
    }

    books.forEach(book => {
        const status = book.is_borrowed ? "Borrowed" : "Available";
        const statusClass = book.is_borrowed ? "tag-borrowed" : "tag-available";
        
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${book.id}</td>
            <td>${book.title}</td>
            <td>${book.author}</td>
            <td>${book.category}</td>
            <td><span class="status-tag ${statusClass}">${status}</span></td>
            <td class="action-cell">
                <button class="tbl-edit-btn" onclick="editBook('${book.id}')">Edit</button>
                <button class="tbl-delete-btn" onclick="deleteBookRow('${book.id}')">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Direct AJAX deletion without reloading the webpage
function deleteBookRow(bookId) {
    if (!confirm("Are you sure you want to permanently delete this book entry?")) return;

    const csrfToken = document.getElementById("csrfToken").value;

    fetch(`/api/books/delete/${bookId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) throw new Error("Failed to delete record.");
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Re-fetch books dynamically to refresh the dataset and look updated immediately
            fetchBooks(document.getElementById("dashboardSearch").value);
            
            // Incrementally update global stat summaries displayed on dashboard cards dynamically
            refreshQuickStats();
        } else {
            alert(data.error || "An error occurred.");
        }
    })
    .catch(error => console.error("Error deleting book record:", error));
}

function editBook(id) {
    window.location.href = `/edit-book/?id=${id}`;
}

// Simple dynamic function to keep upper overview counts updated alongside changes
function refreshQuickStats() {
    fetch("/api/books/")
        .then(res => res.json())
        .then(data => {
            const books = data.books;
            const total = books.length;
            const borrowed = books.filter(b => b.is_borrowed).length;
            const available = total - borrowed;

            document.getElementById("totalBooks").innerText = total;
            document.getElementById("borrowedCount").innerText = borrowed;
            document.getElementById("availableCount").innerText = available;
        });
}