document.addEventListener("DOMContentLoaded", function(){

    const alert = document.getElementById("alert-message");

    if(alert){

        setTimeout(function(){

            alert.classList.add("hide");

            setTimeout(function(){

                alert.remove();

            },500);

        },3000);

    }

});