/* World of Games — JS سبک (بدون وابستگی) — ~2KB */
(function () {
  'use strict';

  // منوی موبایل
  var toggle = document.getElementById('navToggle');
  var nav = document.getElementById('mainNav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // تأیید قبل از عملیات‌های حساس
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (form && form.hasAttribute && form.hasAttribute('data-confirm')) {
      if (!window.confirm(form.getAttribute('data-confirm'))) {
        e.preventDefault();
      }
    }
  }, true);

  // تمام‌صفحه کردن بازی
  var fsBtn = document.getElementById('fullscreenBtn');
  var stage = document.getElementById('playStage');
  if (fsBtn && stage) {
    fsBtn.addEventListener('click', function () {
      if (document.fullscreenElement) {
        document.exitFullscreen();
      } else if (stage.requestFullscreen) {
        stage.requestFullscreen();
      }
    });
  }

  // قفل اسکرول پشت منوی باز در موبایل
  if (toggle) {
    toggle.addEventListener('click', function () {
      document.body.style.overflow = nav && nav.classList.contains('open') ? 'hidden' : '';
    });
  }
})();
