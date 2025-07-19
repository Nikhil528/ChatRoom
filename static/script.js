document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle functionality
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
        
        // Check for saved theme preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            document.body.className = savedTheme;
            updateThemeButton(savedTheme);
        }
    }
});

function toggleTheme() {
    const body = document.body;
    if (body.classList.contains('dark-mode')) {
        body.className = 'light-mode';
        localStorage.setItem('theme', 'light-mode');
        updateThemeButton('light-mode');
    } else {
        body.className = 'dark-mode';
        localStorage.setItem('theme', 'dark-mode');
        updateThemeButton('dark-mode');
    }
}

function updateThemeButton(theme) {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.textContent = theme === 'dark-mode' ? '☀️' : '🌙';
    }
}
