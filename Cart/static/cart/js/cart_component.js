
window.addToCart = function(itemId) {
    fetch('/api/cart/add/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
        body: JSON.stringify({'item_id': itemId})
    }).then(r => r.json()).then(d => {
        if(d.status === 'success') {
            window.refreshBasketUI();
            window.openBasket();
        } else { alert(d.message); }
    });
};

document.addEventListener('DOMContentLoaded', () => {
    const openBasketBtn = document.getElementById('open-basket-btn');
    const basketSidebar = document.getElementById('basket-sidebar');
    const basketOverlay = document.getElementById('basket-overlay');
    const confirmBtn = document.getElementById('confirmOrderBtn');

    window.openBasket = function() {
        if(!basketSidebar || !basketOverlay) return;
        basketSidebar.classList.add('is-active');
        basketOverlay.classList.add('is-active');
        document.body.classList.add('basket-open');
    };

    window.closeBasket = function() {
        if(!basketSidebar || !basketOverlay) return;
        basketSidebar.classList.remove('is-active');
        basketOverlay.classList.remove('is-active');
        document.body.classList.remove('basket-open');
    };

    if(openBasketBtn) openBasketBtn.addEventListener('click', window.openBasket);
    if(basketOverlay) basketOverlay.addEventListener('click', window.closeBasket);
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && basketSidebar && basketSidebar.classList.contains('is-active')) {
            window.closeBasket();
        }
    });

    window.refreshBasketUI = function() {
        const listContainer = document.getElementById('cart-list-container');
        const totalDisplay = document.getElementById('cart-total-display');

        if(!listContainer) return;

        fetch('/api/cart/update/')
        .then(response => response.json())
        .then(data => {
            listContainer.innerHTML = '';

            if (data.items.length === 0) {
                listContainer.innerHTML = '<p style="text-align:center; padding:20px; color:#888;">Your basket is empty.</p>';
                totalDisplay.innerText = '₱ 0.00';
                confirmBtn.disabled = true;
                return;
            }
            confirmBtn.disabled = false;

            data.items.forEach(item => {
                const li = document.createElement('li');
                li.className = 'basket-item';
                li.innerHTML = `
                    <img src="${item.img}" class="item-image" alt="${item.name}">
                    <div class="item-details">
                        <p class="item-name">${item.name}</p>
                        <span class="item-price">₱ ${item.price.toFixed(2)}</span>
                        <span class="item-subtext">Take Out</span>
                    </div>
                    <div class="item-actions">
                        <div class="quantity-selector">
                            <span class="quantity-value">${item.qty}</span>
                            <button class="qty-btn" data-id="${item.id}" onclick="updateCartQty(this, 1)">+</button>
                            <button class="qty-btn" data-id="${item.id}" onclick="updateCartQty(this, -1)">-</button>
                        </div>
                    </div>
                `;
                listContainer.appendChild(li);
            });

            totalDisplay.innerText = '₱ ' + data.total.toLocaleString('en-US', {minimumFractionDigits: 2});
        })
        .catch(error => {
             listContainer.innerHTML = '<p style="text-align:center; padding:20px; color:red;">Failed to load cart.</p>';
             console.error('Error fetching cart:', error)
        });
    };

    if(confirmBtn) {
        confirmBtn.addEventListener('click', () => {
            if(confirmBtn.disabled) return;

            fetch('/api/cart/checkout/', {
                method: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json'}
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    window.location.href = "/history/";
                } else {
                    alert(data.message || "Error processing order.");
                }
            })
            .catch(error => console.error('Error during checkout:', error));
        });
    }

    // Initial Load
    window.refreshBasketUI();
});

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

function updateCartQty(btn, change) {
    const itemId = btn.getAttribute('data-id');

    fetch('/api/cart/change_qty/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
        body: JSON.stringify({'item_id': itemId, 'change': change})
    })
    .then(r => r.json())
    .then(d => {
        if (d.status === 'success' || d.status === 'deleted') {
            window.refreshBasketUI(); // Reload the whole basket display
        } else {
            alert(d.message || "Failed to update quantity.");
        }
    });
}