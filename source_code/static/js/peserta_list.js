// peserta_list.js - DataTable and dark mode toggle logic for peserta_list.html

document.addEventListener('DOMContentLoaded', function() {
  // DataTable initialization
  if (window.jQuery && $('#datapeserta').length) {
    $('#datapeserta').DataTable();
  }
  // Dark mode toggle logic
  const toggle = document.getElementById('theme-toggle');
  const sunIcon = document.getElementById('sun-icon');
  const moonIcon = document.getElementById('moon-icon');
  if (localStorage.getItem('theme') === 'dark') {
    document.documentElement.classList.add('dark');
    if (toggle) toggle.checked = true;
    if (sunIcon) sunIcon.classList.add('hidden');
    if (moonIcon) moonIcon.classList.remove('hidden');
  } else {
    document.documentElement.classList.remove('dark');
    if (toggle) toggle.checked = false;
    if (sunIcon) sunIcon.classList.remove('hidden');
    if (moonIcon) moonIcon.classList.add('hidden');
  }
  if (toggle) {
    toggle.addEventListener('change', function() {
      if (toggle.checked) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
        if (sunIcon) sunIcon.classList.add('hidden');
        if (moonIcon) moonIcon.classList.remove('hidden');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
        if (sunIcon) sunIcon.classList.remove('hidden');
        if (moonIcon) moonIcon.classList.add('hidden');
      }
    });
  }
});
