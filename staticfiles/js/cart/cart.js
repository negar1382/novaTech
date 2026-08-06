// افزایش تعداد
document.querySelectorAll(".increase-btn").forEach(function(btn){

    btn.addEventListener("click", function(){

        fetch(this.dataset.url,{

            method:"POST",

            headers:{
                "X-CSRFToken":this.dataset.csrf,
                "X-Requested-With":"XMLHttpRequest"
            }

        })

        .then(response=>response.json())

        .then(data=>{
            console.log(data);
            if(data.success){

                const quantity = this.parentElement.querySelector(".qty-number");

                quantity.innerText = data.quantity;

                document.getElementById("subtotal-price").innerText =
                    data.subtotal + " تومان";

                document.getElementById("discount-price").innerText =
                    data.discount + " تومان";

                document.getElementById("shipping-price").innerText =
                    data.shipping;

                document.getElementById("final-price").innerText =
                    data.final_price + " تومان";

            }

        });

    });

});



// کاهش تعداد
document.querySelectorAll(".decrease-btn").forEach(function(btn){

    btn.addEventListener("click", function(){

        fetch(this.dataset.url,{

            method:"POST",

            headers:{
                "X-CSRFToken":this.dataset.csrf,
                "X-Requested-With":"XMLHttpRequest"
            }

        })

        .then(response=>response.json())

        .then(data=>{
            console.log(data);
            if(data.success){

                if(data.deleted){

                    location.reload();

                }else{

                    const quantity = this.parentElement.querySelector(".qty-number");

                    quantity.innerText = data.quantity;

                    document.getElementById("subtotal-price").innerText =
                    data.subtotal + " تومان";

                    document.getElementById("discount-price").innerText =
                        data.discount + " تومان";

                    document.getElementById("shipping-price").innerText =
                        data.shipping;

                    document.getElementById("final-price").innerText =
                        data.final_price + " تومان";

                }

            }

        });

    });

});



// حذف محصول
document.querySelectorAll(".remove-btn").forEach(function(btn){

    btn.addEventListener("click", function(){

        fetch(this.dataset.url,{

            method:"POST",

            headers:{
                "X-CSRFToken":this.dataset.csrf,
                "X-Requested-With":"XMLHttpRequest"
            }

        })

        .then(response=>response.json())

        .then(data=>{
            console.log(data);
            if(data.success){

                const cartItem = this.closest(".cart-item");

                if(cartItem){

                    cartItem.remove();

                }

                document.getElementById("subtotal-price").innerText =
                    data.subtotal + " تومان";

                document.getElementById("discount-price").innerText =
                    data.discount + " تومان";

                document.getElementById("shipping-price").innerText =
                    data.shipping;

                document.getElementById("final-price").innerText =
                    data.final_price + " تومان";

                if(document.querySelectorAll(".cart-item").length === 0){

                    location.reload();

                }

            }

        });

    });

});