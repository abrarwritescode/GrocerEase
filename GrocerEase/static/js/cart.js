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
        deleteCartItem(itemId);
    } else {
        return false;
    }
}

function deleteCartItem(itemId) {
    console.log('User is authenticated, sending data...');

    var url = '/deletecart/' + itemId + '/';

    fetch(url, {
        method: 'POST', 
        headers: {
            'X-CSRFToken': csrftoken, 
        },
    })
    .then((response) => {
        if (response.status === 200) {
            
            location.reload(); 
        } else {
            
            console.error('Deletion failed');
        }
    });
}
