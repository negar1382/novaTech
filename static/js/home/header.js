const menuBtn = document.querySelector(".mobile-menu-btn");

const mobileMenu = document.querySelector(".mobile-menu");

const overlay = document.querySelector(".mobile-menu-overlay");

const closeBtn = document.querySelector(".mobile-menu-close");



function openMenu(){

    mobileMenu.classList.add("active");

    overlay.classList.add("active");

}



function closeMenu(){

    mobileMenu.classList.remove("active");

    overlay.classList.remove("active");

}



if(menuBtn){

    menuBtn.addEventListener("click", openMenu);

}


if(closeBtn){

    closeBtn.addEventListener("click", closeMenu);

}


if(overlay){

    overlay.addEventListener("click", closeMenu);

}




// باز و بسته کردن دسته بندی‌ها

const categoryBtn = document.querySelector(".mobile-category button");

const categoryList = document.querySelector(".mobile-category-list");



if(categoryBtn){

    categoryBtn.addEventListener("click",()=>{

        categoryList.classList.toggle("active");

    });

}