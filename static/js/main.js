/**
 * Swayamsevak Foundation - Client-side Scripts
 */

document.addEventListener('DOMContentLoaded', function () {
  'use strict';

  // 1. Auto-dismiss Bootstrap Alerts after 7 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      try {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      } catch (e) {
        // Fallback
        alert.style.display = 'none';
      }
    }, 7000);
  });

  // 2. Client-side Phone Input Formatter / Sanitizer
  const phoneInputs = document.querySelectorAll('input[type="tel"], input[name="phone"]');
  phoneInputs.forEach(function (input) {
    input.addEventListener('input', function (e) {
      // Allow only digits, plus, and spaces
      this.value = this.value.replace(/[^\d+]/g, '');
    });
  });

  // 3. Navbar scroll shadow enhancement
  const navbar = document.querySelector('.navbar-custom');
  if (navbar) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 15) {
        navbar.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.08)';
      } else {
        navbar.style.boxShadow = 'var(--shadow-sm)';
      }
    });
  }

  // 4. Accessible keyboard navigation enhancement for dropdowns
  const dropdownElements = document.querySelectorAll('.dropdown-toggle');
  dropdownElements.forEach(function (dropdown) {
    dropdown.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') {
        const menu = this.nextElementSibling;
        if (menu) {
          const firstItem = menu.querySelector('.dropdown-item');
          if (firstItem) {
            firstItem.focus();
            e.preventDefault();
          }
        }
      }
    });
  });
});
