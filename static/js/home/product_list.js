document.addEventListener('DOMContentLoaded', function () {

  /* ========================================
     ۱) باز/بسته کردن بلوک‌های فیلتر (قیمت، راهنمای خرید، سازنده)
  ======================================== */
  document.querySelectorAll('.filter-block__header').forEach(function (header) {
    header.addEventListener('click', function () {
      const block = header.closest('.filter-block');
      block.classList.toggle('is-collapsed');
    });
  });

  /* ========================================
     ۲) اسلایدر بازه‌ی قیمت (دو دستگیره)
  ======================================== */
  const minInput = document.getElementById('priceMin');
  const maxInput = document.getElementById('priceMax');
  const fill = document.getElementById('priceRangeFill');
  const minLabel = document.getElementById('priceMinLabel');
  const maxLabel = document.getElementById('priceMaxLabel');

  if (minInput && maxInput && fill) {

    const persianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    function toPersianDigits(num) {
      return String(num).replace(/[0-9]/g, function (d) {
        return persianDigits[d];
      });
    }

    function formatPrice(num) {
      return toPersianDigits(Number(num).toLocaleString('en-US'));
    }

    function updateSlider() {
      const min = parseInt(minInput.min, 10);
      const max = parseInt(minInput.max, 10);
      let minVal = parseInt(minInput.value, 10);
      let maxVal = parseInt(maxInput.value, 10);

      // جلوگیری از عبور دستگیره‌ها از هم
      if (minVal > maxVal - 1) {
        minVal = maxVal - 1;
        minInput.value = minVal;
      }

      const minPercent = ((minVal - min) / (max - min)) * 100;
      const maxPercent = ((maxVal - min) / (max - min)) * 100;

      fill.style.right = minPercent + '%';
      fill.style.left = (100 - maxPercent) + '%';

      minLabel.textContent = formatPrice(minVal);
      maxLabel.textContent = formatPrice(maxVal);
    }

    minInput.addEventListener('input', updateSlider);
    maxInput.addEventListener('input', updateSlider);
    updateSlider();
  }

  /* ========================================
     ۳) دکمه‌ی فلش هر محصول (باز کردن گزینه‌های بیشتر)
     فعلا فقط چرخش آیکون رو مدیریت می‌کنه؛ محتوای بازشونده رو
     می‌تونی بعدا (مثلا رنگ‌ها/حافظه‌های مختلف محصول) اضافه کنی.
  ======================================== */
  document.querySelectorAll('.product-row__expand').forEach(function (btn) {
    btn.addEventListener('click', function () {
      btn.classList.toggle('is-open');
    });
  });

});