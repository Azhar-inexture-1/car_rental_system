fetch("http://127.0.0.1:8000/orders/config/")
.then((result) => { return result.json(); })
.then((data) => {
    console.log('publish key: ', data.publishable_key);
    const stripe = Stripe(data.publishable_key, {
        stripeAccount: {YOUR_STRIPE_ACCOUNT}
    });
})
.catch((error) => {
    console.log(error);
});