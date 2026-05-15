function searchBooks() {
    const input = document.getElementById("searchInput");
    if (!input) return;
    
    const query = input.value.toLowerCase();
    const books = document.querySelectorAll(".gallery a");

    books.forEach(book => {
        const title = book.querySelector("p")?.textContent.toLowerCase() || "";
        if (title.includes(query)) {
            book.style.display = "inline-block";
        } else {
            book.style.display = "none";
        }
    });
}