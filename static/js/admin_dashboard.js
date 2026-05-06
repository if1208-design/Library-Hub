document.addEventListener("DOMContentLoaded", function () {

    const savedUser = JSON.parse(localStorage.getItem("user"));
    if (!savedUser || savedUser.isAdmin !== "true") {
        alert("Access denied!");
        window.location.href = "/login/";
        return;
    }

    renderBooks();
    updateStats();
});

function renderBooks() {
    const books = JSON.parse(localStorage.getItem("books")) || [];
    const borrowedBooks = JSON.parse(localStorage.getItem("borrowedBooks")) || [];
    const tableBody = document.getElementById("bookTableBody");
    tableBody.innerHTML = "";

    if (books.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="6">No books available</td></tr>`;
        return;
    }

    books.forEach(book => {
        const isBorrowed = borrowedBooks.includes(book.id);
        const status = isBorrowed ? "Borrowed" : "Available";
        const statusClass = isBorrowed ? "tag-borrowed" : "tag-available";
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${book.id}</td>
            <td>${book.name}</td>
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
}

function deleteBook(id) {
    if (!confirm("Are you sure you want to delete this book?")) return;
    let books = JSON.parse(localStorage.getItem("books")) || [];
    let borrowedBooks = JSON.parse(localStorage.getItem("borrowedBooks")) || [];
    books = books.filter(book => book.id !== id);
    borrowedBooks = borrowedBooks.filter(b => b !== id);
    localStorage.setItem("books", JSON.stringify(books));
    localStorage.setItem("borrowedBooks", JSON.stringify(borrowedBooks));
    renderBooks();
    updateStats();
}

function editBook(id) {
    window.location.href = `/edit-book/?id=${id}`;
}

function updateStats() {
    const books = JSON.parse(localStorage.getItem("books")) || [];
    const borrowedBooks = JSON.parse(localStorage.getItem("borrowedBooks")) || [];
    const users = JSON.parse(localStorage.getItem("users")) || [];
    document.getElementById("totalBooks").innerText = books.length;
    document.getElementById("borrowedCount").innerText = borrowedBooks.length;
    document.getElementById("availableCount").innerText = books.length - borrowedBooks.length;
    document.getElementById("userCount").innerText = users.length;
}

function logout() {
    localStorage.removeItem("user");
    window.location.href = "/login/";
}
