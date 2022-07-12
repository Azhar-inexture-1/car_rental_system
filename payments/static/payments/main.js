const element = document.querySelector('#error-handling');

fetch("/payments/config/")
.then((result) => { return result.json(); })
.then((data) => {

    const stripe = Stripe(data.publishable_key);
    
    document.querySelector("#checkout").addEventListener("click", () => {

        var start_date = document.getElementById("start-date").value;
        var end_date = document.getElementById("end-date").value;
        var car_id = document.getElementById("car-id").value;
        var jwt_token = document.getElementById("jwt-token").value;
        var discount_coupon = document.getElementById("discount").value;

        fetch("/payments/checkout-session/", {
     
            // Adding method type
            method: "POST",
             
            // Adding body or contents to send
            body: JSON.stringify({
                start_date: start_date,
                end_date: end_date,
                car: car_id,
                stripe_discount_id: discount_coupon
            }),
             
            // Adding headers to the request
            headers: {
                "Authorization": "Bearer " + jwt_token,
                "Content-type": "application/json",
            }
        })
        .then(async response => {
            const isJson = response.headers.get('content-type')?.includes('application/json');
            const data = isJson && await response.json();
    
            // check for error response
            if (!response.ok) {
                // get error message from body or default to response status
                const error = (data && data.message) || response.status;
                return Promise.reject(error);
            }
    
            return stripe.redirectToCheckout({sessionId: data.sessionId})
        })
        .catch(error => {
            element.innerHTML = `Error: ${error}`;
            console.error('There was an error!', error);
        });
    });
})
.catch((error) => {
    console.log(error);
});