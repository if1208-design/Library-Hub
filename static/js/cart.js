let cart = JSON.parse(localStorage.getItem('cart')) || [];

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

function updateCartCount() {
    const cartBadge = document.getElementById('cart-count');
    if (cartBadge) {
        cartBadge.innerText = cart.length;
        cartBadge.style.display = cart.length > 0 ? 'inline-block' : 'none';
    }
}

function addToCart(bookId, type, price) {
    const existing = cart.find(function(item) {
        return item.id === bookId && item.type === type;
    });
    
    if (existing) {
        alert('This item is already in your cart!');
        return;
    }
    
    cart.push({
        id: bookId,
        type: type,
        price: price
    });
    
    saveCart();
    alert('Added to cart!');
}

function removeFromCart(index) {
    cart.splice(index, 1);
    saveCart();
    if (window.location.pathname.includes('/cart/')) {
        displayCart();
    }
}

function displayCart() {
    const container = document.getElementById('cart-items');
    if (!container) return;
    
    if (cart.length === 0) {
        container.innerHTML = '<p style="text-align: center;">Your cart is empty 🛒</p>';
        document.getElementById('cart-total').innerHTML = '0 EGP';
        return;
    }
    
    let html = '<table><thead><tr><th>Book</th><th>Type</th><th>Price</th><th>Action</th></tr></thead><tbody>';
    let total = 0;
    
    for (let i = 0; i < cart.length; i++) {
        const item = cart[i];
        const book = booksData[item.id];
        if (book) {
            const priceValue = parseFloat(item.price);
            total = total + priceValue;
            html = html + '<tr>' +
                '<td>' + (book.name || book.title) + '</td>' +
                '<td>' + (item.type === 'borrow' ? 'Borrow' : 'Buy') + '</td>' +
                '<td>' + item.price + ' EGP' + '</td>' +
                '<td><button onclick="removeFromCart(' + i + ')">Remove</button>' + '</td>' +
                '</tr>';
        }
    }
    
    html = html + '</tbody></table>';
    container.innerHTML = html;
    document.getElementById('cart-total').innerHTML = total + ' EGP';
}

function goToCheckout() {
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }
    sessionStorage.setItem('checkoutCart', JSON.stringify(cart));
    window.location.href = '/checkout/';
}

document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    if (window.location.pathname.includes('/cart/')) {
        displayCart();
    }
});