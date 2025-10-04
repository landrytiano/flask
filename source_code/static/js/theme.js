// theme.js - Dark mode toggle and persistence
document.addEventListener('DOMContentLoaded', function() {
  // Check for toggle checkbox
  const toggleCheckbox = document.getElementById('theme-toggle');
  
  // Set initial state based on localStorage
  function applyTheme() {
    const savedTheme = localStorage.getItem('darkMode') || 'light';
    
    if (savedTheme === 'dark') {
      document.documentElement.classList.add('dark');
      if (toggleCheckbox) toggleCheckbox.checked = true;
    } else {
      document.documentElement.classList.remove('dark');
      if (toggleCheckbox) toggleCheckbox.checked = false;
    }
  }
  
  // Apply theme on load
  applyTheme();
  
  // Global function for toggle
  window.toggleDarkMode = function() {
    const isDark = document.documentElement.classList.contains('dark');
    if (isDark) {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('darkMode', 'light');
      if (toggleCheckbox) toggleCheckbox.checked = false;
    } else {
      document.documentElement.classList.add('dark');
      localStorage.setItem('darkMode', 'dark');
      if (toggleCheckbox) toggleCheckbox.checked = true;
    }
  };
});
