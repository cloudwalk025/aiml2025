// static/js/payment.js
document.addEventListener('DOMContentLoaded', function() {
    const paymentForm = document.getElementById('payment-form');
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const paymentMethod = document.querySelector('input[name="payment_method"]:checked').value;
            
            if (paymentMethod === 'credit_card') {
                // Create Stripe token
                Stripe.setPublishableKey('{{ stripe_public_key }}');
                
                Stripe.card.createToken({
                    number: document.getElementById('card-number').value,
                    cvc: document.getElementById('card-cvc').value,
                    exp_month: document.getElementById('card-expiry-month').value,
                    exp_year: document.getElementById('card-expiry-year').value
                }, stripeResponseHandler);
            } else if (paymentMethod === 'paypal') {
                // For PayPal, we'd normally redirect to PayPal
                // Here we just submit the form
                document.getElementById('stripeToken').value = 'paypal_' + Math.random().toString(36).substr(2, 9);
                paymentForm.submit();
            }
        });
    }
});

function stripeResponseHandler(status, response) {
    const paymentForm = document.getElementById('payment-form');
    
    if (response.error) {
        // Show errors
        document.getElementById('payment-errors').textContent = response.error.message;
    } else {
        // Add token to form and submit
        const tokenInput = document.createElement('input');
        tokenInput.setAttribute('type', 'hidden');
        tokenInput.setAttribute('name', 'stripeToken');
        tokenInput.setAttribute('value', response.id);
        paymentForm.appendChild(tokenInput);
        
        // Submit form
        paymentForm.submit();
    }
}