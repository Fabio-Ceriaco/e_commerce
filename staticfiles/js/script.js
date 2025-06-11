document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('menu-button');
    const menu = button.nextElementSibling;

    button.addEventListener('click', function(event) {
        event.preventDefault();
        menu.classList.toggle('hidden');
    });

    // Optional: Hide dropdown when clicking outside
    document.addEventListener('click', function(event) {
        if (!button.contains(event.target) && !menu.contains(event.target)) {
            menu.classList.add('hidden');
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('profile-menu');
    const menu = button.nextElementSibling;

    button.addEventListener('click', function(event) {
        event.preventDefault();
        menu.classList.toggle('hidden');
    });

    // Optional: Hide dropdown when clicking outside
    document.addEventListener('click', function(event) {
        if (!button.contains(event.target) && !menu.contains(event.target)) {
            menu.classList.add('hidden');
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('dash-menu');
    const menu = button.nextElementSibling;

    button.addEventListener('click', function(event) {
        event.preventDefault();
        menu.classList.toggle('hidden');
    });

    // Optional: Hide dropdown when clicking outside
    document.addEventListener('click', function(event) {
        if (!button.contains(event.target) && !menu.contains(event.target)) {
            menu.classList.add('hidden');
        }
    });
});

