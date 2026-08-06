const mainImage = document.getElementById("mainProductImage");

const thumbnails = document.querySelectorAll(".thumbnail");

thumbnails.forEach(function(item){

    item.addEventListener("click", function(){

        mainImage.src = this.src;

    });

});


// لایک
const likeBtn = document.getElementById("like-btn");
const url = likeBtn.dataset.url;
const csrf = likeBtn.dataset.csrf;

if (likeBtn){

    likeBtn.addEventListener("click", function(){



            fetch(url, {

                method: "POST",

                headers: {
                    "X-CSRFToken": csrf
                }

            })

        .then(response=>response.json())

        .then(data=>{

            if(data.success){

                const icon=document.getElementById("heart-icon");

                const count=document.getElementById("like-text");

                count.innerText=data.likes_count;

                if(data.liked){

                    icon.classList.remove("fa-regular");
                    icon.classList.add("fa-solid");
                    icon.classList.add("liked");

                }else{

                    icon.classList.remove("fa-solid");
                    icon.classList.remove("liked");
                    icon.classList.add("fa-regular");add("fa-regular");

                }

            }

        });

    });

}



// افزایش تعداد
const increaseBtn = document.getElementById("increase-btn");

if (increaseBtn){

    increaseBtn.addEventListener("click", function(){

        fetch(this.dataset.url,{

            method:"POST",

            headers:{
                "X-CSRFToken":this.dataset.csrf,
                "X-Requested-With":"XMLHttpRequest"
            }

        })

        .then(response=>response.json())

        .then(data=>{

            if(data.success){
                const badge = document.getElementById("cart-badge");

                if (badge){
                    badge.innerText = data.cart_count;
                }

                document.getElementById("quantity-number").innerText=data.quantity;

            }

        });

    });

}



// کاهش تعداد
const decreaseBtn=document.getElementById("decrease-btn");

if(decreaseBtn){

    decreaseBtn.addEventListener("click",function(){

        fetch(this.dataset.url,{

            method:"POST",

            headers:{
                "X-CSRFToken":this.dataset.csrf,
                "X-Requested-With":"XMLHttpRequest"
            }

        })

        .then(response=>response.json())

        .then(data=>{

            if(data.success){
                const badge = document.getElementById("cart-badge");

                if (badge){
                    badge.innerText = data.cart_count;
                }

                if(data.deleted){

                    document.getElementById("quantity-section").style.display = "none";

                    document.getElementById("add-cart-btn").style.display = "flex";

                    document.getElementById("quantity-number").innerText = 1;

                //     پاک کردن url دکمه ها
                    document.getElementById("increase-btn").removeAttribute("data-url");

                    document.getElementById("decrease-btn").removeAttribute("data-url");

                }else{

                    document.getElementById("quantity-number").innerText=data.quantity;

                }

            }

        });

    });

}


// افزودن به سبد خرید
const addCartBtn = document.getElementById("add-cart-btn");

if (addCartBtn){

    addCartBtn.addEventListener("click", function(){

        fetch(this.dataset.url, {

            method: "POST",

            headers: {
                "X-CSRFToken": this.dataset.csrf,
                "X-Requested-With": "XMLHttpRequest"
            }

        })

        .then(response => response.json())

        .then(data => {

            if(data.success){
                const badge = document.getElementById("cart-badge");

                if (badge){
                    badge.innerText = data.cart_count;
                }

                // مخفی شدن دکمه افزودن
                addCartBtn.style.display = "none";

                // نمایش بخش تعداد
                document.getElementById("quantity-section").style.display = "flex";

                // قرار دادن تعداد روی ۱
                document.getElementById("quantity-number").innerText = data.quantity;

                document.getElementById("increase-btn").dataset.url =
                    data.increase_url;

                document.getElementById("decrease-btn").dataset.url =
                    data.decrease_url;

            }

        });

    });

}