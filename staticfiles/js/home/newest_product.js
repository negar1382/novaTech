document.addEventListener("DOMContentLoaded", function () {

    // روی تمام کاروسل‌های صفحه اجرا می‌شود
    document.querySelectorAll(".new-arrivals__carousel").forEach(function (carousel) {

        const list = carousel.querySelector(".new-arrivals__list");
        const arrowRight = carousel.querySelector(".carousel-arrow--right");
        const arrowLeft = carousel.querySelector(".carousel-arrow--left");

        if (!list || !arrowRight || !arrowLeft) return;

        function getCardWidth() {
            const card = list.querySelector(".na-card");
            if (!card) return 240;

            const gap = parseFloat(getComputedStyle(list).gap) || 16;

            return card.offsetWidth + gap;
        }

        arrowLeft.addEventListener("click", function () {
            list.scrollBy({
                left: -getCardWidth() * 3,
                behavior: "smooth"
            });
        });

        arrowRight.addEventListener("click", function () {
            list.scrollBy({
                left: getCardWidth() * 3,
                behavior: "smooth"
            });
        });

        function updateArrows() {

            const maxScroll = list.scrollWidth - list.clientWidth;
            const current = Math.abs(list.scrollLeft);

            if (maxScroll <= 5) {
                arrowLeft.classList.add("is-hidden");
                arrowRight.classList.add("is-hidden");
                return;
            }

            if (current <= 5)
                arrowRight.classList.add("is-hidden");
            else
                arrowRight.classList.remove("is-hidden");

            if (current >= maxScroll - 5)
                arrowLeft.classList.add("is-hidden");
            else
                arrowLeft.classList.remove("is-hidden");
        }

        list.addEventListener("scroll", updateArrows);
        window.addEventListener("resize", updateArrows);

        updateArrows();

    });

});