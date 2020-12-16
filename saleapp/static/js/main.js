function addToCart(id, name, gia) {
    fetch('/api/cart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": gia
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        location.reload()
        var stats = document.getElementById('cart-stats')
        var total_number = document.getElementById('total_number')
        var number = document.getElementById('number_quantity')
        var total_price = document.getElementById('total_price')
        total_number.innerText = '${data.total_quantity}';
        total_price.innerText = '${data.total_amount} VNĐ';
//        var cart = document.getElementById("cart-info");
        number.innerText = '${data.total_quantity}';
//        cart.innerText = `${data.total_quantity} - ${data.total_amount} VNĐ`;
    }).catch(err => {
        console.log(err);
    })

    // promise --> await/async
}

function pay() {
    fetch('/api/pay', {
        method: 'post',
        headers: {
            'Context-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert(data.message);
        location.reload();
    }).catch(err => {
        location.href = '/login1?next=/payment';
    });
}