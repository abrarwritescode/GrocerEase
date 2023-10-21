var updateBtns = document.getElementsByClassName('update-cart');
var user = '{{ customer_data|safe }}';

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('Button clicked. Product ID:', productId, 'Action:', action);
        console.log('Customer:', user);

        updateUserOrder(productId, action);  
    });
}

function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...');

    var url = '/updatecart/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'productId': productId, 'action': action }),
    })
    .then((response) => {
        console.log('Request sent. Waiting for response...');
        return response.json();
    })
    .then((data) => {
        console.log('Response received:', data);
        location.reload();
    });
}

function confirmDelete(itemId) {
    if (confirm('Are you sure you want to delete this item from your cart?')) {
        // The user clicked OK, so proceed with item deletion
        deleteCartItem(itemId);
    } else {
        // The user clicked Cancel, so do nothing
        return false;
    }
}

function deleteCartItem(itemId) {
    console.log('User is authenticated, sending data...');

    var url = '/deletecart/' + itemId + '/';

    fetch(url, {
        method: 'POST', // You can use 'DELETE' if your Django view handles DELETE requests
        headers: {
            'X-CSRFToken': csrftoken, // Make sure to include your CSRF token
        },
    })
    .then((response) => {
        if (response.status === 200) {
            // Deletion was successful
            location.reload(); // Refresh the cart or update it as needed
        } else {
            // Handle the case where deletion failed
            console.error('Deletion failed');
        }
    });
}
