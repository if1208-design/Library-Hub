// ===== GET BOOKS FROM STORAGE =====
function getBooks() {
    return JSON.parse(localStorage.getItem("books")) || [];
}

// ===== SAVE BOOKS =====
function saveBooks(books) {
    localStorage.setItem("books", JSON.stringify(books));
}

// ===== ADD BOOK =====
function addBook(event) {
    event.preventDefault();

    const id = document.querySelector('[name="book_id"]').value;
    const name = document.querySelector('[name="book_name"]').value;
    const author = document.querySelector('[name="author"]').value;
    const category = document.querySelector('[name="category"]').value;
    const description = document.querySelector('textarea').value;

    let books = getBooks();

    // check if ID exists
    if (books.find(book => book.id == id)) {
        alert("Book ID already exists!");
        return;
    }

    books.push({ id, name, author, category, description });
    saveBooks(books);

    alert("Book added successfully ✅");
    document.querySelector("form").reset();
}

// ===== LOAD BOOK FOR EDIT =====
function loadBook() {
    const idInput = document.querySelector('[name="book_id"]');

    idInput.addEventListener("blur", () => {
        let books = getBooks();
        let book = books.find(b => b.id == idInput.value);

        if (book) {
            document.querySelector('[name="book_name"]').value = book.name;
            document.querySelector('[name="author"]').value = book.author;
            document.querySelector('[name="category"]').value = book.category;
            document.querySelector('textarea').value = book.description;
        } else {
            alert("Book not found ❌");
        }
    });
}

// ===== UPDATE BOOK =====
function updateBook(event) {
    event.preventDefault();

    const id = document.querySelector('[name="book_id"]').value;
    let books = getBooks();

    let index = books.findIndex(b => b.id == id);

    if (index === -1) {
        alert("Book not found ❌");
        return;
    }

    books[index] = {
        id,
        name: document.querySelector('[name="book_name"]').value,
        author: document.querySelector('[name="author"]').value,
        category: document.querySelector('[name="category"]').value,
        description: document.querySelector('textarea').value
    };

    saveBooks(books);

    alert("Book updated successfully ✨");
}