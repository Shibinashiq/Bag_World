
var paymentMethodRadios = document.querySelectorAll('input[name="payment-method"]');
const form = document.getElementById("checkoutForm")
const totalamount = document.getElementById("totalamount")

console.log(totalamount)

const bankRadio = document.getElementById('bank');
    // Add a change event listener to each radio button
    let id
    paymentMethodRadios.forEach(function(radio) {
        radio.addEventListener('change', function() {

            // Log the value of the selected payment method
            id=this.value
            console.log('Selected Payment Method:', this.value,id);
            if (this.value === 'bank') {
                console.log("this is id", this.value);
                razorpay();
            }
        
        });
    });

    

function razorpay() {
   


            var options = {
                "key": "rzp_test_WHOEXgrD9IAr4I",
                "amount":100,
                "currency": "INR",
                "name": "Bag world",
                "description": "Thanks for buying from us",
                "image": "https://example.com/your_logo",
                // "order_id": "order_IluGWxBm9U8zJ8",
                "handler": function(responseb) {
                    console.log(responseb);
                    alert(responseb.razorpay_payment_id);
                    alert(responseb.razorpay_order_id);
                    alert(responseb.razorpay_signature);

                  
                }
            };


            var rzp1 = new Razorpay(options);
            rzp1.open();
  


    
}
