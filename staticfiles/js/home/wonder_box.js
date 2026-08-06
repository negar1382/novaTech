document.addEventListener('DOMContentLoaded', function () {

  /* ========================================
     ۱) تایمر شمارش معکوس
     ---------------------------------------
     data-end-time روی المنت #countdown خونده میشه (یک تاریخ/ساعت ISO).
     میتونی این مقدار رو از جنگو با {{ campaign.end_time|date:"c" }} پر کنی.
  ======================================== */

  const countdownEl = document.getElementById('countdown');

  if (countdownEl) {

    const endTimeStr = countdownEl.getAttribute('data-end-time');
    const endTime = endTimeStr
      ? new Date(endTimeStr).getTime()
      : (Date.now() + 25 * 3600 * 1000 + 28 * 60 * 1000 + 10 * 1000);

    const hoursEl = document.getElementById('cd-hours');
    const minutesEl = document.getElementById('cd-minutes');
    const secondsEl = document.getElementById('cd-seconds');

    // تبدیل اعداد انگلیسی به فارسی
    const persianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];

    function toPersianDigits(num) {
      return String(num).replace(/[0-9]/g, function (d) {
        return persianDigits[d];
      });
    }

    function pad(num) {
      return num < 10 ? '0' + num : String(num);
    }

    // ابتدا متغیر را تعریف می‌کنیم
    let timerInterval;

    function updateCountdown() {

      const now = Date.now();
      const diff = endTime - now;

      if (diff <= 0) {

        hoursEl.textContent = toPersianDigits('00');
        minutesEl.textContent = toPersianDigits('00');
        secondsEl.textContent = toPersianDigits('00');

        // فقط اگر تایمر ساخته شده باشد آن را متوقف کن
        if (timerInterval) {
          clearInterval(timerInterval);
        }

        return;
      }

      const totalSeconds = Math.floor(diff / 1000);

      const hours = Math.floor(totalSeconds / 3600);
      const minutes = Math.floor((totalSeconds % 3600) / 60);
      const seconds = totalSeconds % 60;

      hoursEl.textContent = toPersianDigits(pad(hours));
      minutesEl.textContent = toPersianDigits(pad(minutes));
      secondsEl.textContent = toPersianDigits(pad(seconds));
    }

    // اولین بروزرسانی
    updateCountdown();

    // سپس تایمر ساخته می‌شود
    timerInterval = setInterval(updateCountdown, 1000);
  }

  /* ========================================
     ۲) اسکرول محصولات با کلیک روی فلش
     ---------------------------------------
     هر بار کلیک، به اندازه‌ی عرض ۳ کارت محصول اسکرول میشه.
  ======================================== */

  const productsList = document.getElementById('productsList');
  const scrollArrow = document.getElementById('scrollArrow');

  if (productsList && scrollArrow) {

    // عرض تقریبی هر کارت
    function getCardWidth() {
      const firstCard = productsList.querySelector('.product-card');
      return firstCard ? firstCard.getBoundingClientRect().width : 230;
    }

    scrollArrow.addEventListener('click', function () {

      const scrollAmount = getCardWidth() * 3;

      productsList.scrollBy({
        left: -scrollAmount,
        behavior: 'smooth'
      });

    });

    // مخفی کردن فلش در انتهای اسکرول
    function updateArrowVisibility() {

      const maxScroll = productsList.scrollWidth - productsList.clientWidth;
      const currentScroll = Math.abs(productsList.scrollLeft);

      if (maxScroll <= 5) {
        scrollArrow.classList.add('is-hidden');
      }
      else if (currentScroll >= maxScroll - 5) {
        scrollArrow.classList.add('is-hidden');
      }
      else {
        scrollArrow.classList.remove('is-hidden');
      }

    }

    productsList.addEventListener('scroll', updateArrowVisibility);
    window.addEventListener('resize', updateArrowVisibility);

    updateArrowVisibility();
  }

});