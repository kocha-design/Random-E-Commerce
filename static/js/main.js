// =========================================
// 0. AUTO-HIDE MESSAGES (Ile ya awali)
// =========================================
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.messages').forEach(el => {
        setTimeout(() => {
            el.style.transition = 'opacity 0.4s';
            el.style.opacity = '0';
            setTimeout(() => el.remove(), 400);
        }, 5000);
    });
});


// =========================================
// FEATURE 3: TOAST NOTIFICATIONS
// (Tunaweka hii kwanza kwa sababu inatumiwa na Features zingine)
// =========================================
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icon = type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ';
    toast.innerHTML = `
        <span class="toast-icon">${icon}</span>
        <span class="toast-message">${message}</span>
    `;

    container.appendChild(toast);

    // Animate in
    setTimeout(() => toast.classList.add('show'), 10);

    // Auto-remove after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}


// =========================================
// FEATURE 1: ADD TO CART (AJAX / BILA KUREFRESH)
// =========================================
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.add-to-cart-form');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const btn = form.querySelector('button[type="submit"]');
        const originalText = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner"></span> Adding...';

        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateCartCounter(data.cart_count);
                showToast(data.message, 'success');
            } else {
                showToast(data.message || 'Error adding to cart', 'error');
            }
        })
        .catch(err => {
            showToast('Something went wrong. Please try again.', 'error');
            console.error(err);
        })
        .finally(() => {
            btn.disabled = false;
            btn.innerHTML = originalText;
        });
    });
});

// Update cart counter kwenye header
function updateCartCounter(count) {
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        cartCount.textContent = count + ' item' + (count !== 1 ? 's' : '');
        cartCount.classList.add('bump');
        setTimeout(() => cartCount.classList.remove('bump'), 300);
    }
}


// =========================================
// FEATURE 2: LIVE SEARCH
// =========================================
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    if (!searchInput || !searchResults) return;

    let debounceTimer;

    searchInput.addEventListener('input', function() {
        const q = this.value.trim();
        clearTimeout(debounceTimer);

        if (q.length < 2) {
            searchResults.innerHTML = '';
            searchResults.classList.remove('active');
            return;
        }

        debounceTimer = setTimeout(() => {
            fetch(`/products/search-ajax/?q=${encodeURIComponent(q)}`)
                .then(r => r.json())
                .then(data => {
                    if (data.results.length === 0) {
                        searchResults.innerHTML = '<div class="no-results">No products found</div>';
                    } else {
                        searchResults.innerHTML = data.results.map(p => `
                            <a href="${p.url}" class="search-result-item">
                                ${p.image ? `<img src="${p.image}" alt="${p.name}">` : '<div class="no-img">📦</div>'}
                                <div>
                                    <strong>${p.name}</strong>
                                    <small>TSh ${parseFloat(p.price).toLocaleString()}</small>
                                </div>
                            </a>
                        `).join('');
                    }
                    searchResults.classList.add('active');
                })
                .catch(err => console.error(err));
        }, 300);
    });

    // Funga search results unapobonyeza nje
    document.addEventListener('click', function(e) {
        if (!e.target.closest('#searchForm')) {
            searchResults.classList.remove('active');
        }
    });
});


// =========================================
// FEATURE 4: LOADING SPINNER KWENYE FORMS
// =========================================
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form.form-card');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const btn = form.querySelector('button[type="submit"]');
            if (btn && !btn.dataset.loading) {
                btn.dataset.loading = 'true';
                const originalText = btn.innerHTML;
                btn.innerHTML = '<span class="spinner"></span> Loading...';
                btn.disabled = true;

                // Rudisha kama kuna kosa (baada ya sekunde 5)
                setTimeout(() => {
                    if (btn.dataset.loading === 'true') {
                        btn.innerHTML = originalText;
                        btn.disabled = false;
                        btn.dataset.loading = 'false';
                    }
                }, 5000);
            }
        });
    });
});


// =========================================
// FEATURE 5: IMAGE GALLERY (THUMBNAILS)
// =========================================
function changeImage(url, btn) {
    const mainImage = document.getElementById('mainImage');
    if (mainImage) {
        mainImage.style.opacity = '0';
        setTimeout(() => {
            mainImage.src = url;
            mainImage.style.opacity = '1';
        }, 150);
    }
    
    document.querySelectorAll('.thumb').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
}