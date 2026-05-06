//load available books
function getBooks() {
    return JSON.parse(localStorage.getItem("books")) || [];
}

function booksTableA() {
    const tableBody = document.getElementById("tbodyA");
    const books = getBooks();
    //clear old existing rows
    tableBody.innerHTML = "";
    if (books.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="5">Library empty!</td></tr>';
        return;
    }
    else{
        books.forEach(book => {
        const row = document.createElement("tr");

        row.innerHTML = 
            '<td>'+book.id+'</td>' +
            '<td>'+book.name+'</td>' +
            '<td>'+book.category+'</td>' +
            '<td>'+book.author+'</td>';
        tableBody.appendChild(row);
    });
    }
}

//to intialize display when the page loads
document.addEventListener("DOMContentLoaded", booksTableA);