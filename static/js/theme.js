document.addEventListener("DOMContentLoaded", function() {
  const toggleButton = document.getElementById('theme-toggle');
  const darkIcon = document.getElementById('dark-icon');
  const lightIcon = document.getElementById('light-icon');
  
  // ตรวจสอบ theme ที่บันทึกไว้ก่อนหน้า
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    darkIcon.style.display = 'none';
    lightIcon.style.display = 'block';
  }
  
  // เมื่อคลิกปุ่มเปลี่ยนธีม
  toggleButton.addEventListener('click', function() {
    if (document.documentElement.getAttribute('data-theme') === 'dark') {
      document.documentElement.setAttribute('data-theme', 'light');
      localStorage.setItem('theme', 'light');
      darkIcon.style.display = 'block';
      lightIcon.style.display = 'none';
    } else {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
      darkIcon.style.display = 'none';
      lightIcon.style.display = 'block';
    }
  });
});