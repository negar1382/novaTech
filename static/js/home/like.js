const likeBtn = document.getElementById("like-btn");

if (likeBtn){

    likeBtn.addEventListener("click", function(){

        fetch("{% url 'toggle_product_like' product.id %}",{

            method:"POST",

            headers:{
                "X-CSRFToken":"{{ csrf_token }}"
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

                }else{

                    icon.classList.remove("fa-solid");

                    icon.classList.add("fa-regular");

                }

            }

        });

    });

}
