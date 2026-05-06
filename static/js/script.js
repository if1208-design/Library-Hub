const booksData = {
    "1": { id: "1", name: "واحة اليعقوب", author: "Amr Abdelhamid", category: "Fiction", description: "A dark fantasy set in a mysterious oasis where humans are born without eyelids.", img: "book1.jpeg", price: "270 EGP", fee: "75 EGP" },
    "2": { id: "2", name: "مينتو", author: "Mohamed Ibrahim", category: "Psychology", description: "A psychological narrative exploring human behavior and emotional struggles.", img: "book2.jpeg", price: "180 EGP", fee: "75 EGP" },
    "3": { id: "3", name: "سماء بلا ضياء", author: "Khawla Hamdi", category: "Fiction", description: "A story about a mysterious land without sunlight and hidden knowledge.", img: "book3.jpeg", price: "320 EGP", fee: "75 EGP" },
    "4": { id: "4", name: "ما رواهُ البحر", author: "Ahmed Alaa Eldin", category: "Fiction", description: "A reflective story about memories, emotions, and human relationships.", img: "book4.jpeg", price: "200 EGP", fee: "75 EGP" },
    "5": { id: "5", name: "في ممر الفئران", author: "Ahmed Khaled Tawfik", category: "Science", description: "A dystopian world where sunlight disappears, forcing humanity to live in darkness.", img: "book5.jpeg", price: "220 EGP", fee: "75 EGP" },
    "6": { id: "6", name: "عقدك النفسية سجنك الأبدي", author: "Youssef Alhassan", category: "Psychology", description: "Explains how unresolved psychological complexes control behavior.", img: "book6.jpeg", price: "150 EGP", fee: "75 EGP" },
    "7": { id: "7", name: "قوانين التحرر من الصراع النفسي", author: "Ahmed Emara", category: "Psychology", description: "A guide to understanding and overcoming internal psychological conflicts.", img: "book7.jpg", price: "160 EGP", fee: "75 EGP" },
    "8": { id: "8", name: "جلسات نفسية", author: "Mohamed Ibrahim", category: "Psychology", description: "A collection of simplified psychological insights.", img: "book8.jpg", price: "140 EGP", fee: "75 EGP" },
    "9": { id: "9", name: "مُحاط بالمرضى النفسيين", author: "Thomas Erikson", category: "Psychology", description: "Explains how to identify and deal with manipulative personality types.", img: "book9.jpg", price: "300 EGP", fee: "75 EGP" },
    "10": { id: "10", name: "مُمتلئ بالفراغ", author: "Imad Rashad Othman", category: "Psychology", description: "A psychological exploration of addiction and inner emptiness.", img: "book10.jpg", price: "180 EGP", fee: "75 EGP" },
    "11": { id: "11", name: "الجَلاد تحت جِلدي", author: "Imad Rashad Othman", category: "Psychology", description: "Exploration of self-criticism and perfectionism.", img: "book11.jpg", price: "200 EGP", fee: "75 EGP" },
    "12": { id: "12", name: "أحببت وغدًا", author: "Imad Rashad Othman", category: "Psychology", description: "Focuses on healing from toxic and narcissistic relationships.", img: "book12.jpg", price: "170 EGP", fee: "75 EGP" },
    "13": { id: "13", name: "فاتتني صلاة", author: "Islam Gamal", category: "History", description: "Explains psychological reasons behind neglecting prayer.", img: "book13.jpg", price: "120 EGP", fee: "75 EGP" },
    "14": { id: "14", name: "اعرف وجهك الآخر", author: "Youssef Al-Hassani", category: "Psychology", description: "Explores hidden aspects of personality and relationships.", img: "book14.jpg", price: "140 EGP", fee: "75 EGP" },
    "15": { id: "15", name: "اصنع وقتًا أكثر من المتاح", author: "Jake Knapp", category: "Science", description: "A practical system to redesign daily habits.", img: "book15.jpg", price: "250 EGP", fee: "75 EGP" },
    "16": { id: "16", name: "خلاصة علم النفس", author: "Ali Al-Wardi", category: "Psychology", description: "Introduces core psychological ideas about human behavior.", img: "book16.jpg", price: "140 EGP", fee: "75 EGP" },
    "17": { id: "17", name: "حضارة العرب", author: "Gustave Le Bon", category: "History", description: "A historical study of Arab achievements.", img: "book17.jpg", price: "180 EGP", fee: "75 EGP" },
    "18": { id: "18", name: "وداعًا طليطلة", author: "Naguib Al-Kilani", category: "Fiction", description: "A historical novel portraying the fall of Andalusia.", img: "book18.jpg", price: "160 EGP", fee: "75 EGP" },
    "19": { id: "19", name: "ثلاثية غرناطة", author: "Radwa Ashour", category: "History", description: "Follows generations of a family after the fall of Granada.", img: "book19.jpg", price: "250 EGP", fee: "75 EGP" },
    "20": { id: "20", name: "حضارة بابل وآشور", author: "Mahmoud Khairat", category: "History", description: "Explores ancient Mesopotamian civilizations.", img: "book20.jpg", price: "170 EGP", fee: "75 EGP" }
};

function getAllBooks() {
    const adminBooksArr = JSON.parse(localStorage.getItem("books")) || [];
    const combinedBooks = { ...booksData };
    adminBooksArr.forEach(book => {
        if (book.id) combinedBooks[book.id] = book;
    });
    return combinedBooks;
}

function displayBooksInHome() {
    const allBooks = getAllBooks();
    const galleries = {
        "Fiction": document.getElementById("gallery-Fiction"),
        "Psychology": document.getElementById("gallery-Psychology"),
        "Science": document.getElementById("gallery-Science"),
        "History": document.getElementById("gallery-History"),
        "Others": document.getElementById("gallery-Others")
    };

    Object.values(allBooks).forEach(book => {
        if (!document.querySelector(`[data-id="${book.id}"]`)) {
            let cat = book.category || "Others";
            let targetKey = "Others";

            if (cat.includes("Fiction")) targetKey = "Fiction";
            else if (cat.includes("Psychology")) targetKey = "Psychology";
            else if (cat.includes("Science")) targetKey = "Science";
            else if (cat.includes("History")) targetKey = "History";

            let targetGallery = galleries[targetKey] || galleries["Others"];
            if (targetGallery) {
                targetGallery.innerHTML += `
                    <a href="/book-details/?id=${book.id}" data-id="${book.id}">
                        <img src="${book.img || 'default-book.png'}" alt="${book.name || 'Book'}">
                    </a>`;
            }
        }
    });
}

function handleBorrow() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');
    let borrowed = JSON.parse(localStorage.getItem("borrowedBooks")) || [];
    if (borrowed.includes(id)) { alert("You already borrowed this!"); return; }
    borrowed.push(id);
    localStorage.setItem("borrowedBooks", JSON.stringify(borrowed));
    window.location.href = "/borrowed-books/";
}

function handleReturn(button, id) {
    let borrowed = JSON.parse(localStorage.getItem("borrowedBooks")) || [];
    borrowed = borrowed.filter(bid => bid !== id.toString());
    localStorage.setItem("borrowedBooks", JSON.stringify(borrowed));
    button.parentElement.parentElement.remove();
}

window.onload = function () {
    const allBooks = getAllBooks();
    const params = new URLSearchParams(window.location.search);
    const currentId = params.get('id');
    let borrowed = JSON.parse(localStorage.getItem("borrowedBooks")) || [];

    let btn = document.getElementById("borrow-btn");
    if (borrowed.includes(currentId) && btn) {
        btn.innerText = "Already Borrowed";
        btn.style.backgroundColor = "gray";
    }

    if (window.location.pathname === "/" || window.location.pathname.includes("/home/")) {
        displayBooksInHome();
    }

    if (window.location.pathname.includes("/borrowed-books/")) {
        let tbody = document.querySelector("table tbody");
        if (tbody) {
            tbody.innerHTML = "";
            borrowed.forEach(id => {
                const b = allBooks[id];
                if (b) {
                    let d = new Date();
                    let r = new Date(); r.setDate(d.getDate() + 14);
                    tbody.innerHTML += `<tr><td>${b.id}</td><td>${b.name || b.title}</td><td>${d.toLocaleDateString()}</td><td>${r.toLocaleDateString()}</td><td><button onclick="handleReturn(this, '${b.id}')">Return</button></td></tr>`;
                }
            });
        }
    }

    if (window.location.pathname.includes("/book-details/")) {
        const book = allBooks[currentId];
        if (book) {
            document.getElementById('bookName').innerText = book.name || book.title;
            document.getElementById('bookImg').src = book.img;
            document.getElementById('bookIdDisplay').innerText = book.id;
            document.getElementById('bookAuthor').innerText = book.author;
            document.getElementById('bookCategory').innerText = book.category;
            document.getElementById('bookDescription').innerText = book.description || book.desc;
            if (document.getElementById('bookPrice')) document.getElementById('bookPrice').innerText = book.price;
            if (document.getElementById('bookBorrowFee')) document.getElementById('bookBorrowFee').innerText = book.fee;
        }
    }
};

function searchBooks() {
    const input = document.getElementById("searchInput").value.toLowerCase();
    const books = document.querySelectorAll(".gallery a");

    books.forEach(book => {
        const title = book.getAttribute("data-title")?.toLowerCase() || "";
        const author = book.getAttribute("data-author")?.toLowerCase() || "";

        if (title.includes(input) || author.includes(input)) {
            book.style.display = "inline-block";
        } else {
            book.style.display = "none";
        }
    });
}

function handleBuy() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');
    if (id) window.location.href = `/checkout/?id=${id}`;
}