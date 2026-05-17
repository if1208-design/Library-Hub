<<<<<<< HEAD
document.addEventListener('DOMContentLoaded', function () {

  const input = document.getElementById('searchInput');
  if (!input) return;

  input.addEventListener('input', function () {
    const query = input.value.toLowerCase().trim();
    const filter = document.querySelector('.search-dropdown')?.value || 'title';

    const books = document.querySelectorAll('.gallery a');

    books.forEach(book => {
      const title = book.querySelector('p')?.textContent.toLowerCase() || '';
      const match = title.includes(query);
      book.style.display = match ? '' : 'none';
    });

    // إخفاء اسم الكاتيجوري لو كل كتبها اتخفت
    document.querySelectorAll('.category-title').forEach(cat => {
      const gallery = cat.nextElementSibling;
      if (!gallery || !gallery.classList.contains('gallery')) return;
      const visible = [...gallery.querySelectorAll('a')].some(b => b.style.display !== 'none');
      cat.style.display = visible ? '' : 'none';
      gallery.style.display = visible ? '' : 'none';
    });
  });

});
=======
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
>>>>>>> 6b32eed1fbe78acae92717f3229ec7f4d7991a37
