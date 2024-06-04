// checkout.js

// Get the total order amount from the server
var total = '{{order.get_cart_total}}';

// Set up PayPal payment button
paypal.Buttons({
    // Set up the transaction
    createOrder: function(data, actions) {
        return actions.order.create({
            purchase_units: [{
                amount: {
                    value: parseFloat(total).toFixed(2) // Convert total to a float and fix to 2 decimal places
                }
            }]
        });
    },

    // Finalize the transaction
    onApprove: function(data, actions) {
        return actions.order.capture().then(function(details) {
            submitFormData(); // Call the function to submit form data
        });
    }
}).render('#paypal-button-container'); // Render PayPal button in specified container

// Get shipping status from the server
var shipping = '{{order.shipping}}';

// If shipping is disabled, remove shipping information section from the DOM
if (shipping == 'False') {
    document.getElementById('shipping-info').innerHTML = '';
}

// Add event listener to the form submission
var form = document.getElementById('form');
form.addEventListener('submit', function(e) {
    e.preventDefault();
    console.log('Form Submitted...');
    document.getElementById('form-button').classList.add("hidden"); // Hide form button
    document.getElementById('payment-info').classList.remove("hidden"); // Show payment info
});

// Function to submit form data
function submitFormData() {
    console.log('Payment button clicked');


    // Gather shipping information if shipping is enabled
    var shippingInfo = {
        'address': null,
        'city': null,
        'state': null,
        'zipcode': null,
    };

    if (shipping != 'False') {
        shippingInfo.address = form.address.value;
        shippingInfo.city = form.city.value;
        shippingInfo.state = form.state.value;
        shippingInfo.zipcode = form.zipcode.value;
    }

    console.log('Shipping Info:', shippingInfo);
    console.log('User Info:', userFormData);

    // Send form data to server for processing
    var url = "/process_order/";
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'applicaiton/json',
            'X-CSRFToken': csrftoken, // Include CSRF token
        },
        body: JSON.stringify({
            'form': userFormData,
            'shipping': shippingInfo
        }),

    }).then((response) => response.json())
        .then((data) => {
            console.log('Success:', data);
            alert('Transaction completed'); // Show success message

            // Reset cart and redirect to store page
            cart = {};
            document.COOKIE = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";

            window.location.href = "{% url 'store' %}"; // Redirect to store page
        });
}

